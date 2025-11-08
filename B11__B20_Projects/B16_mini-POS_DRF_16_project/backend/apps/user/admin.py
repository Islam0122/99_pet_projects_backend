from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "fullname", "email", "role", "is_allowed")

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('username', 'fullname', 'role', 'email', 'is_allowed', 'is_active',)
    search_fields = ('username', 'fullname', 'email')
    list_filter = ('is_allowed', 'is_active', 'is_staff')
    readonly_fields = ('date_joined',)
    filter_horizontal = ()
    filter_vertical = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'role', 'email', 'is_allowed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_random_password_and_notify()
        obj.save()

    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'fullname', 'role',
                'email', 'is_allowed', 'is_active', 'is_staff'
            )
        }),
        ('Дополнительные параметры', {'fields': ('date_joined',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

