from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


# note :
# username = None: username 필드를 사용하지 않음을 명시.
# USERNAME_FIELD = "email": 이메일을 사용자 이름 필드로 사용하여 인증.
# REQUIRED_FIELDS = []: 이메일 외에 추가로 필수적인 필드가 없음을 설정
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=4)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
