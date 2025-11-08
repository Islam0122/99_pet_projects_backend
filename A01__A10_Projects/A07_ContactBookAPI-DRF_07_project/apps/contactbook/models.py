import uuid
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ContactBook(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Уникальный идентификатор"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец контакта",
        help_text="Пользователь, которому принадлежит этот контакт"
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Введите имя контакта"
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Введите фамилию контакта (опционально)"
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Электронная почта",
        help_text="Укажите email (необязательно)"
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона в международном формате"
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Адрес",
        help_text="Укажите адрес (необязательно)"
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Теги",
        help_text="Укажите теги через запятую, например: друзья, работа, семья"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
        help_text="Когда контакт был создан"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Когда контакт был изменён"
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or "Без имени"
