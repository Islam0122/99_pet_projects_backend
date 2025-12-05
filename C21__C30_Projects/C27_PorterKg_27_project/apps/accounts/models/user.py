
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..managers.user_manager import UserManager


class AuthType(models.TextChoices):
    """Типы аутентификации"""
    LOCAL = 'local', 'Local'
    GOOGLE = 'google', 'Google'


class UserRole(models.TextChoices):
    """Роли пользователей"""
    ADMIN = 'admin', 'Admin'
    DRIVER = 'driver', 'Driver'
    GUEST = 'guest', 'Guest'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Email адрес'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден'
    )
    auth_type = models.CharField(
        max_length=10,
        choices=AuthType.choices,
        default=AuthType.LOCAL,
        verbose_name='Тип аутентификации'
    )
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.GUEST,
        verbose_name='Роль'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Персонал'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_driver(self):
        return self.role == UserRole.DRIVER

    def is_guest(self):
        return self.role == UserRole.GUEST