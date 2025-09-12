import logging
from django.db import models

logger = logging.getLogger(__name__)

# ===========================
# Базовая модель с датами
# ===========================
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True