from django.db import models
from django.contrib.auth.models import User
from checking.models import Member
from django.db.models import Model


class MemberCheck(models.Model):
    name = models.ForeignKey(
        Member,
        related_name="membercheck",
        on_delete=models.CASCADE,
        to_field="name",
    )
    status = models.CharField(max_length=500, null=True, default=None)
    pray_member = models.CharField(max_length=300, null=True, default=None)
    date = models.DateTimeField()


class UserCheck(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="usercheck",
        to_field="username",
    )
    worship = models.CharField(max_length=3, null=True, default=None)  # 예/아니오
    meeting = models.CharField(max_length=3, null=True, default=None)  # 예/아니오
    qt = models.CharField(max_length=3, null=True, default=None)  # 01회
    pray_time = models.CharField(max_length=4, null=True, default=None)  # 001분
    pray_youth = models.CharField(
        max_length=300, null=True, default=None
    )  # 청소년부를 위한 기도
    pray_group = models.CharField(
        max_length=300, null=True, default=None
    )  # 반 모임을 위한 기도
    pray_user = models.CharField(max_length=300, null=True, default=None)  # 사용자에 대한 기도
    pray_emergency = models.CharField(max_length=300, null=True, default=None)  # 긴급 기도
    date = models.DateTimeField()  # 작성일 기준 이전 주일 입력
