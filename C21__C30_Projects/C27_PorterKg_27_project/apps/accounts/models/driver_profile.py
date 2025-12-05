from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .user import User


class DriverProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='driver_profile',
        verbose_name='Пользователь'
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=20,
        verbose_name='Номер телефона'
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )

    rating = models.FloatField(
        default=100.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ],
        verbose_name='Рейтинг'
    )
    total_trips = models.PositiveIntegerField(
        default=0,
        verbose_name='Всего поездок'
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        verbose_name='Стаж вождения (лет)'
    )
    verified_driver = models.BooleanField(
        default=False,
        verbose_name='Верифицированный водитель'
    )

    driver_license_number = models.CharField(
        max_length=50,
        verbose_name='Номер водительского удостоверения'
    )
    driver_license_category = models.CharField(
        max_length=10,
        verbose_name='Категория ВУ'
    )
    driver_license_expiry = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания ВУ'
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
        verbose_name = 'Профиль водителя'
        verbose_name_plural = 'Профили водителей'
        ordering = ['-rating', '-created_at']
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['verified_driver']),
        ]

    def __str__(self):
        return f"Водитель: {self.user.full_name} (Рейтинг: {self.rating})"

    @property
    def has_complete_profile(self):
        return bool(
            self.phone_number and
            self.driver_license_number and
            self.driver_license_category and
            hasattr(self, 'car')
        )

    def update_rating(self, new_rating):
        total_trips = self.total_trips or 1
        self.rating = (self.rating * total_trips + new_rating) / (total_trips + 1)
        self.save(update_fields=['rating'])

    def increment_trips(self):
        self.total_trips += 1
        self.save(update_fields=['total_trips'])