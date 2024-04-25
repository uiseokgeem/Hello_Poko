from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="members",
        to_field="username",
    )  # to_field : 외래키로 지정된 모델의 특정 필드값을 참조할 수 있게함.
    name = models.CharField(max_length=5)  # 최대로 넣을 수 있는 글자 수
    grade = models.CharField(max_length=3, null=True, default=None)
    gender = models.CharField(max_length=3, null=True, default=None)
    attendance = models.IntegerField(default=0)  # 값이 없는 경우 default = 0
    absent = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attendance", to_field="username"
    )
    name = models.CharField(max_length=50)  # 최대로 넣을 수 있는 글자 수
    attendance = models.CharField(max_length=50)
    date = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GetImage(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True)  # upload_to="checking/getimage/%Y/%m/%d"
    description = models.TextField()

    def __str__(self):
        return self.name
