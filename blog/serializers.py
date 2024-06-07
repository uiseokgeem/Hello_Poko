from django.db.models import QuerySet
from rest_framework import serializers

from account.models import CustomUser
from .models import Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, customuser) -> str:
        return f"{customuser.first_name} {customuser.last_name}"

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "username",
        ]


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
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
        ]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all().only("id", "title", "author").select_related("author")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

        fields = [
            "id",
            "message",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    comment_list = CommentSerializer(many=True, source="comment_set")

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "comment_list"]
