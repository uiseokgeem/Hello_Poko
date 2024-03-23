from django.db import models


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=50, unique=True)  # 학년관리
    # grade_code = models.CharField(max_length=50, unique=False)  # member로 빠져야 할 듯

    def __str__(self):  # 제목에 오브젝트가 아니라 이름이 나오도록
        return self.teacher_name

    class Meta:
        ordering = ["-id"]


class Member(models.Model):  # 모델명의 첫글자는 대문자로
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="members",
    )
    name = models.CharField(max_length=5)  # 최대로 넣을 수 있는 글자 수
    grade = models.CharField(max_length=1, null=True, default=None)
    gender = models.CharField(max_length=1, null=True, default=None)
    attendance = models.IntegerField(default=0)  # 값이 없는 경우 default = 0
    absent = models.IntegerField(default=0)

    def __str__(self):  # 제목에 오브젝트가 아니라 이름이 나오도록
        return self.name


class Attendance(models.Model):  # 모델명의 첫글자는 대문자로
    name = models.CharField(max_length=50)  # 최대로 넣을 수 있는 글자 수
    attendance = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    teacher_name = models.CharField(max_length=10)
    # grade_description = models.OneToOneField(Grade, on_delete=models.CASCADE) # OneToOneField 모델

    def __str__(self):
        return self.name


class GetImage(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True)  # upload_to="checking/getimage/%Y/%m/%d"
    description = models.TextField()

    def __str__(self):
        return self.name
