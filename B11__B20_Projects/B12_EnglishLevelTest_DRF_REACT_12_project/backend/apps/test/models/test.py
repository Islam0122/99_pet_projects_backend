from django.db import models
import logging
from .basemodel import BaseModel
from .level import Level
logger = logging.getLogger(__name__)


# ===========================
# Тест (Test)
# ===========================
class Test(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название теста",
        help_text="Название темы теста, например 'Грамматика A1'"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание теста",
        help_text="Описание теста и его особенности"
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        verbose_name="Уровень теста",
        help_text="Выберите уровень CEFR, к которому относится тест"
    )

    def __str__(self):
        return f"{self.name} ({self.level})"

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ['level', 'name']