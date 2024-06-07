from django.db import models
from account.models import CustomUser
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
        CustomUser,
        on_delete=models.CASCADE,
        related_name="usercheck",
        to_field="username",
    )

    title = models.CharField(max_length=30, null=True, default=None)
    worship = models.IntegerField(
        null=True,
        default=None,
        choices=worship_choice,
    )
    qt = models.IntegerField(
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
    pray_emergency = models.CharField(
        max_length=300, null=True, default=None
    )  # 교사 긴급 기도
    issue = models.CharField(max_length=300, null=True, default=None)  # 문의사항/긴급사항
    date = models.DateTimeField()  # 작성일 기준 이전 주일 입력


class Comment(models.Model):
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comment",
        to_field="username",
    )
    member_check = models.ForeignKey(
        MemberCheck, on_delete=models.CASCADE, related_name="comment"
    )
    feedback = models.CharField(max_length=500)
    date = models.DateTimeField()
