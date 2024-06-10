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

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all()


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    # author = serializers.CharField(source="author.username")

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

    #  return Post.objects.all().defer("content").select_related("author")
    # defer를 제외하고 only를 사용하여쿼리셋과 직렬화코드의 필드를 일치 시킨다. -> 쿼리셋과 직렬화의 일치로 가독성 향상과 유지보수성 증가!


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

        fields = [
            "id",
            "message",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    # author = serializers.CharField(source="author.username")

    # comment_list = serializers.StringRelatedField(many=True, source="comment_set") # 역참조 기본
    comment_list = CommentSerializer(
        many=True, source="comment_set"
    )  # 사전 형태의 역참조, CommentSerializer 작성

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "comment_list"]
