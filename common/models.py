from django.db import models
from account.models import CustomUser
from report.models import MemberCheck


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
