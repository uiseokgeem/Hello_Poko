# drf api를 만들기 위한 py
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
)
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
