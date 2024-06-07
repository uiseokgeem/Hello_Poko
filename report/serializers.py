from django.db.models import QuerySet
from rest_framework import serializers
from report.models import UserCheck


class TitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheck
        fields = [
            "id",
            "title",
        ]

    @staticmethod  # -> requset 객체 접근이 필요할 경우 인스턴스 메서드로 전환, 이번 실습에서는 정적 메서드 유지하며 requst 객체에 전달.
    def get_optimized_queryset(request) -> QuerySet[UserCheck]:
        return UserCheck.objects.filter(teacher=request.user).only("id", "title")
