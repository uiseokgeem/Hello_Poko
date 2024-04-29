from django.contrib import admin
from .models import Member, Attendance, GetImage, Register
from django.utils.safestring import mark_safe


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "teacher",
        "name",
        "grade",
        "gender",
        "attendance",
        "absent",
    ]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "teacher", "name", "attendance", "date"]


@admin.register(GetImage)
class GetImageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]

    def photo_tag(self, GetImage):
        if GetImage.image:  # GetImage model 내에 첨부된 사진이 있다면
            return mark_safe(f'<img src="{GetImage.image.url}" style="width: 72px;" />')
        return None

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ["id","name","gender","birth","phone_number","email","address","register_at","funnels"]