from django.db import models
import logging
from .basemodel import BaseModel

logger = logging.getLogger(__name__)


# ===========================
# Уровень (Level)
# ===========================
class Level(BaseModel):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название уровня",
        help_text="Например: A1, B2, C1"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание уровня",
        help_text="Описание уровня, его особенности и навыки"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"
        ordering = ['title']
