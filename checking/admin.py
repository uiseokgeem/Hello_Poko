from django.contrib import admin
from .models import Teacher, Member, Attendance, GetImage
from django.utils.safestring import mark_safe


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher_name")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "teacher",
        "grade_code",
        "name",
        "attendance",
        "absent",
    ]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "attendance", "date", "teacher_name"]


@admin.register(GetImage)
class GetImageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]

    def photo_tag(self, GetImage):
        if GetImage.image:  # GetImage model 내에 첨부된 사진이 있다면
            return mark_safe(f'<img src="{GetImage.image.url}" style="width: 72px;" />')
        return None

    # GetImage.image.url : shell에서 GetImage.object.get(pk=1).image.url로 url 접근할 수 있다.(첨부된 파일이 있는 경우에만 url 접근 가능)
