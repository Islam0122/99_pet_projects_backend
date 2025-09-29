from django.db import models
from ..user.models import TgUser
from ..category.models import Category


class UserRecipe(models.Model):
    user = models.ForeignKey(
        TgUser,
        on_delete=models.CASCADE,
        related_name="user_recipes",
        verbose_name="Пользователь",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_recipes",
        verbose_name="Категория",
    )
    user_text = models.CharField(
        max_length=255, verbose_name="Запрос пользователя (ингредиенты или пожелания)"
    )
    ai_result = models.TextField(
        null=True, blank=True, verbose_name="Сгенерированный рецепт AI"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "user_recipe"
        verbose_name = "Пользовательский рецепт"
        verbose_name_plural = "Пользовательские рецепты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_text} ({self.user.username})"
