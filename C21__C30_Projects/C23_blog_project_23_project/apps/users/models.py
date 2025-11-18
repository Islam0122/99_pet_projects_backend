from django.db import models
from django.contrib.auth.models import User
import secrets


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_tokens')
    token = models.CharField(max_length=256, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Token'
        verbose_name_plural = 'User Tokens'

    def __str__(self):
        return f"{self.user.username} - {self.token[:20]}..."

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(192)[:256]  # urlsafe base64, обрезаем до 256

    @classmethod
    def create_for_user(cls, user):
        token = cls.generate_token()
        return cls.objects.create(user=user, token=token)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile of {self.user.username}"