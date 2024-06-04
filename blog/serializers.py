from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = '__all__' 모든 필드를 불러오는 경우
        fields = [
            "id",
            "title",
            "content",
        ]


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
        ]


class PostDictSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
        ]
