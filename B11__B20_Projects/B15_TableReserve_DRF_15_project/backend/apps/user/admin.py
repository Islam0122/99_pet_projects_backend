from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'role', 'auth_type', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'auth_type', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions',
         {'fields': ('role', 'auth_type', 'is_verified', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'auth_type', 'is_verified', 'is_staff',
                       'is_active')}
         ),
    )
