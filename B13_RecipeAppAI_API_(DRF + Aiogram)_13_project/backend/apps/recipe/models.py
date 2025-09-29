from django.db import models
from ..category.models import Category

class Recipe(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название рецепта"
    )
    description = models.TextField(
        verbose_name="Описание рецепта",
        blank=True
    )
    ingredients = models.TextField(
        verbose_name="Ингредиенты",
        help_text="Список ингредиентов через запятую или в виде текста"
    )
    instructions = models.TextField(
        verbose_name="Инструкция по приготовлению"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recipes",
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        db_table = "recipe"
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["title"]

    def __str__(self):
        return self.title
