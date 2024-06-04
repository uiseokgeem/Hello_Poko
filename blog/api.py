# drf api를 만들기 위한 py
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from blog.models import Post
from blog.serializers import PostSerializer, PostListSerializer, PostDictSerializer


def post_list(request: HttpRequest) -> HttpResponse:
    post_qs = Post.objects.all().defer("content").select_related("author")

    serializer = PostListSerializer(post_qs, many=True)
    list_data: ReturnList = serializer.data
    print(serializer.data)

    return JsonResponse(list_data, safe=False)


# JsonResponse의 인코딩
# post_qs = Post.objects.all() 해당 쿼리셋을 바로 응답 처리 하면
# 이 쿼리셋에 대한 JsonResponse의 인코딩 지원이 없기 때문에
# list(post_qs.values()) 다음과 같이 리스트+사전 조합으로 '직렬화'해야 JsonResponse가 가능하다


def post_detail(request: HttpRequest, pk) -> HttpResponse:
    post_qs = Post.objects.all()
    post = get_object_or_404(post_qs, pk=pk)

    serializer = PostDictSerializer(instance=post)
    detail_data: ReturnDict = serializer.data

    return JsonResponse(detail_data)
