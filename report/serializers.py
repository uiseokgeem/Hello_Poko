from django.db.models import QuerySet
from rest_framework import serializers
from report.models import UserCheck


class TitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheck
        fields = [
            "id",
            "teacher",
            "title",
        ]

    @staticmethod
    def get_optimized_queryset(request) -> QuerySet[UserCheck]:
        return UserCheck.objects.filter(teacher=request.user).only("id", "title")
