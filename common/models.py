from django.db import models
from django.contrib.auth.models import User
from report.models import MemberCheck


class Comment(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment", to_field="username"
    )
    member_check = models.ForeignKey(
        MemberCheck, on_delete=models.CASCADE, related_name="comment"
    )
    feedback = models.CharField(max_length=500)
    date = models.DateTimeField()
