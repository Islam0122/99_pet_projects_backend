from django.contrib import admin
from .models import UserModel, UserProfile

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'is_active', 'is_staff', 'user_registered_at')
    search_fields = ('phone_number', 'email')
    list_filter = ('is_active', 'is_staff')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'subscriptions')
    search_fields = ('first_name', 'last_name')
