from django.contrib import admin
from .models import UserProfile
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(UserProfile)