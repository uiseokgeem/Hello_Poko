from django.contrib import admin
from .models import MemberCheck, UserCheck


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
        "teacher",
        "worship",
        "meeting",
        "qt",
        "pray_time",
        "pray_youth",
        "pray_group",
        "pray_user",
        "pray_emergency",
        "date",
    ]
