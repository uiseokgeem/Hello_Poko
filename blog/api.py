# drf api를 만들기 위한 py
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostSerializer, PostListSerializer, PostDictSerializer
from rest_framework.response import Response
from rest_framework.request import Request

# def post_list(request: HttpRequest) -> HttpResponse:
#     post_qs = Post.objects.all().defer("content").select_related("author")
#
#     serializer = PostListSerializer(post_qs, many=True)
#     list_data: ReturnList = serializer.data
#     print(serializer.data)
#
#     return JsonResponse(list_data, safe=False)


# @api_view(["GET"])
# def post_list(request: Request) -> Response:
#     post_qs = Post.objects.all().defer("content").select_related("author")
#
#     serializer = PostListSerializer(post_qs, many=True)
#     list_data: ReturnList = serializer.data
#     print(serializer.data)
#
#     return Response(list_data)


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
                    "result": response.data,  # ReturnList
                },
                serializer=response.data.serializer,  # response.data.serializer : ReturnDict이 serializer 속성을 지원
            )

        return response


post_list_view = PostListAPIView.as_view()


# JsonResponse의 인코딩
# post_qs = Post.objects.all() 해당 쿼리셋을 바로 응답 처리 하면
# 이 쿼리셋에 대한 JsonResponse의 인코딩 지원이 없기 때문에
# list(post_qs.values()) 다음과 같이 리스트+사전 조합으로 '직렬화'해야 JsonResponse가 가능하다


# def post_detail(request: HttpRequest, pk) -> HttpResponse:
#     post_qs = Post.objects.all()
#     post = get_object_or_404(post_qs, pk=pk)
#     serializer = PostDictSerializer(instance=post)
#     detail_data: ReturnDict = serializer.data
#
#     return JsonResponse(detail_data)

# @api_view(["GET"])
# def post_detail(request: Request, pk) -> Response:
#     post_qs = Post.objects.all()
#     post = get_object_or_404(post_qs, pk=pk)
#     serializer = PostDictSerializer(instance=post)
#     detail_data: ReturnDict = serializer.data
#
#     return Response(detail_data)


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostDictSerializer

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
