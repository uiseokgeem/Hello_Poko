from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict

from blog.models import Post
from blog.serializers import PostListSerializer, PostDetailSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.request import Request


class PostListAPIView(ListAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostListSerializer

    # 응답데이터 구조 변경하기
    def list(self, request: Request, *args, **kwargs):
        response: Response = super().list(request, *args, **kwargs)

        if isinstance(request.accepted_renderer, (JSONRenderer, BrowsableAPIRenderer)):
            response.data = ReturnDict(
                {
                    "ok": True,
                    "result": response.data,
                },
                serializer=response.data.serializer,
            )

        return response


post_list_view = PostListAPIView.as_view()


# JsonResponse의 인코딩
# post_qs = Post.objects.all() 해당 쿼리셋을 바로 응답 처리 하면
# 이 쿼리셋에 대한 JsonResponse의 인코딩 지원이 없기 때문에
# list(post_qs.values()) 다음과 같이 리스트+사전 조합으로 '직렬화'해야 JsonResponse가 가능하다


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostDetailSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        response: Response = super().retrieve(request, *args, **kwargs)

        if isinstance(request.accepted_renderer, (JSONRenderer, BrowsableAPIRenderer)):
            response.data = ReturnDict(
                {
                    "ok": True,
                    "result": response.data,  # ReturnList
                },
                serializer=response.data.serializer,  # response.data.serializer : ReturnDict이 serializer 속성을 지원
            )

        return response


post_detail_view = PostRetrieveAPIView.as_view()


class PostCreateAPIView(
    CreateAPIView
):  # 상속받은 CreateAPIView는 POST 메서드만이 구현되어 있으며 GET 요청에는 405 응답을 한다!
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def peform_create(self, serializer):
        serializer.save(author=self.request.user)


post_new = PostCreateAPIView.as_view()


class PostUpdateAPIView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = PostSerializer.get_optimized_queryset()
    # PostCreateAPIView와 달리 수정할 레코드 조회 과정이 필요하기 떄문에
    # queryset 추가, PostSerializer에도 PostDetailSerializer의 get_optimized_queryset 메서드 추가.


post_edit = PostCreateAPIView.as_view()


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


post_delete = PostDestroyAPIView.as_view()
