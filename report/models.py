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
    gqs = models.BooleanField(default=True)  # GQS 참석 여부
    status = models.CharField(max_length=500, null=True, default=None)
    pray_member = models.CharField(max_length=300, null=True, default=None)
    date = models.DateTimeField()


class UserCheck(models.Model):
    worship_choice = [(0, "불참"), (1, "1부 예배"), (2, "2부 예배"), (3, "3부 예배")]
    qt_choice = [
        (0, "0회"),
        (1, "1회"),
        (2, "2회"),
        (3, "3회"),
        (4, "4회"),
        (5, "5회"),
        (6, "6회"),
        (7, "7회"),
    ]

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="usercheck",
        to_field="username",
    )
    worship = models.IntegerField(
        max_length=3,
        null=True,
        default=None,
        choices=worship_choice,
    )
    qt = models.IntegerField(
        max_length=3,
        null=True,
        default=None,
        choices=qt_choice,
    )
    meeting = models.BooleanField(default=True)  # PM: 참석여부를 default=True로 하기 원함
    pray_youth = models.CharField(
        max_length=300, null=True, default=None
    )  # 청소년부를 위한 기도
    pray_group = models.CharField(
        max_length=300, null=True, default=None
    )  # 반 모임을 위한 기도
    pray_user = models.CharField(max_length=300, null=True, default=None)  # 사용자에 대한 기도
    issue = models.IntegerField(max_length=300, null=True, default=None)  # 문의사항/긴급사항
    date = models.DateTimeField()  # 작성일 기준 이전 주일 입력

    # pray_emergency = models.CharField(max_length=300, null=True, default=None)  # 교사 긴급 기도 보류
    # pray_time = models.CharField(max_length=4, null=True, default=None)  # 교사 사용자 기도 시간 보류
