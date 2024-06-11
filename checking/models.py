from django.db import models
from accounts.models import CustomUser


class Member(models.Model):
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="members",
        to_field="email",
    )  # to_field : 외래키로 지정된 모델의 특정 필드값을 참조할 수 있게함.
    name = models.CharField(max_length=5, unique=True)  # 최대로 넣을 수 있는 글자 수
    grade = models.CharField(max_length=3, null=True, default=None)
    gender = models.CharField(max_length=3, null=True, default=None)
    attendance_count = models.IntegerField(default=0)  # 값이 없는 경우 default = 0
    absent_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    name = models.ForeignKey(
        to="Member",
        on_delete=models.CASCADE,
        related_name="attendance",
        to_field="name",
    )
    attendance = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return self.name.name
        # return self.name 시 오류


class GetImage(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True)  # upload_to="checking/getimage/%Y/%m/%d"
    description = models.TextField()

    def __str__(self):
        return self.name


# 기획서 매핑 후 모델 반영
# class Register(models.Model):
#     name = models.CharField(verbose_name = '이름',max_length=10)
#     GENDERS = (
#         ('M','남성'),
#         ('F','여성')
#     )
#     gender = models.CharField(verbose_name = '성별',max_length=2, choices = GENDERS)
#     birth = models.DateField(verbose_name="생년월일")
#     #휴대폰 정규식
#     phone_regex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
#     phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
#     email = models.EmailField(verbose_name="이메일", max_length=128, unique=True)
#     address = models.TextField(verbose_name="주소지")
#     register_at = models.DateField(verbose_name="신청 날짜")
#     funnels = models.TextField(verbose_name="접하게 된 경로")
#
#     def __str__(self):
#         return self.name
