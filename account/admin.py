from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "username", "email", "full_name", "is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "full_name", "birth_date", "email")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "birth_date",
                    "full_name",
                ),
            },
        ),
    )
