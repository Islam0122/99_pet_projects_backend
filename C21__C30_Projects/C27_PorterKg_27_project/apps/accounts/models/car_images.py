from django.db import models
from .car import Car


class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Автомобиль'
    )

    image = models.ImageField(
        upload_to='car_images/%Y/%m/%d/',
        verbose_name='Изображение'
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name='Главное изображение'
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Изображение автомобиля'
        verbose_name_plural = 'Изображения автомобилей'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['car', 'is_primary']),
        ]

    def __str__(self):
        return f"Изображение для {self.car}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.car.images.exists():
            self.is_primary = True
        super().save(*args, **kwargs)

    def set_as_primary(self):
        CarImage.objects.filter(car=self.car).update(is_primary=False)
        self.is_primary = True
        self.save(update_fields=['is_primary'])