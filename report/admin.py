from django.contrib import admin
from .models import MemberCheck, UserCheck, Comment


@admin.register(MemberCheck)  # Register your models here.
class MemberCheckAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "status",
        "pray_member",
        "date",
    ]


@admin.register(UserCheck)
class UserCheckAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "teacher",
        "worship",
        "meeting",
        "qt",
        "pray_youth",
        "pray_group",
        "pray_user",
        "pray_emergency",
        "date",
    ]


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "teacher", "member_check", "feedback", "date"]
