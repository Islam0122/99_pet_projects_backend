from django.db import models
from django.core.validators import RegexValidator
from .user import User


class GuestProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='guest_profile',
        verbose_name='Пользователь'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        verbose_name='Номер телефона'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Профиль гостя'
        verbose_name_plural = 'Профили гостей'
        ordering = ['-created_at']

    def __str__(self):
        return f"Профиль гостя: {self.user.email}"

    @property
    def has_complete_profile(self):
        return bool(
            self.phone_number and
            self.birth_date
        )