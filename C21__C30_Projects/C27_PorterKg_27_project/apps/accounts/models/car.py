from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .driver_profile import DriverProfile


class FuelType(models.TextChoices):
    """Типы топлива"""
    PETROL = 'petrol', 'Бензин'
    DIESEL = 'diesel', 'Дизель'
    ELECTRIC = 'electric', 'Электро'
    HYBRID = 'hybrid', 'Гибрид'
    GAS = 'gas', 'Газ'


class Car(models.Model):
    driver = models.OneToOneField(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Водитель'
    )

    marka = models.CharField(
        max_length=50,
        verbose_name='Марка'
    )
    model = models.CharField(
        max_length=50,
        verbose_name='Модель'
    )
    color = models.CharField(
        max_length=30,
        verbose_name='Цвет'
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ],
        verbose_name='Год выпуска'
    )

    number_plate = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер автомобиля'
    )
    vin_code = models.CharField(
        max_length=17,
        blank=True,
        verbose_name='VIN-код'
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
        default=FuelType.PETROL,
        verbose_name='Тип топлива'
    )
    max_passengers = models.PositiveIntegerField(
        default=4,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20)
        ],
        verbose_name='Максимум пассажиров'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
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
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['number_plate']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.marka} {self.model} ({self.number_plate})"

    @property
    def full_name(self):
        return f"{self.marka} {self.model} {self.year}"

    @property
    def has_images(self):
        return self.images.exists()

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])