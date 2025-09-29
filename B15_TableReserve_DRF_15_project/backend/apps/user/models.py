from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

AUTH_CHOICES = (
    ('local', 'Local'),
    ('google', 'Google'),
)
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    auth_type = models.CharField(max_length=10, choices=AUTH_CHOICES, default='local')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
