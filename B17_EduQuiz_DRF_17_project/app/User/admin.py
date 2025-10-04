from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'fullname', 'email', 'is_allowed',)
    search_fields = ('username', 'fullname', 'email')
    list_filter = ('is_allowed', 'is_active', 'is_staff')
    readonly_fields = ('date_joined',)
    filter_horizontal = ()
    filter_vertical = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'email', 'is_allowed', 'password1', 'password2')}
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_random_password_and_notify()
        obj.save()

    fieldsets = (
        (None, {'fields': ('username', 'password', 'fullname', 'email', 'is_allowed', 'is_active', 'is_staff')}),  # Убираем 'groups'
        ('Дополнительные параметры', {'fields': ('date_joined',)}),
    )

# Регистрируем модель с одним кастомным админом
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

