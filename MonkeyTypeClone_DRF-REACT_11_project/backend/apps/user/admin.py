from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", "username", "email", "auth_type",
        "best_wpm", "average_accuracy", "is_staff", "is_active"
    )
    list_filter = ("auth_type", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "auth_type")}),
        ("Typing Stats", {"fields": ("best_wpm", "average_accuracy")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "auth_type", "is_active", "is_staff"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")
