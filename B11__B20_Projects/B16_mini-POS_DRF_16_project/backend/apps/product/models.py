from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории (например: Напитки, Десерты, Основные блюда)"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Product(models.Model):
    image = models.ImageField(
        upload_to='products/%Y/%m',
        verbose_name="Фотография товара",
        help_text="Загрузите изображение товара"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Название товара",
        help_text="Введите наименование товара"
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Краткое описание товара"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию, к которой относится товар"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Цена товара без скидки"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена со скидкой",
        help_text="Укажите цену товара со скидкой (если есть)"
    )
    identification_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Уникальный ID товара",
        help_text="Введите уникальный код или артикул товара"
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name="В архиве",
        help_text="Отметьте, если товар больше не продаётся"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Когда товар был добавлен"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Когда товар последний раз редактировался"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.identification_number})"





