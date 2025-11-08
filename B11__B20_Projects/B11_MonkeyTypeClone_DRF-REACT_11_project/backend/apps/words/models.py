from django.db import models

class Timer(models.Model):
    seconds = models.IntegerField(
        verbose_name="Секунды",
        help_text="Введите количество секунд для таймера"
    )

    class Meta:
        db_table = "timers"
        verbose_name = "Таймер"
        verbose_name_plural = "Таймеры"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", help_text="Введите название категории")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Text(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="texts", verbose_name="Категория")
    text_content = models.TextField(verbose_name="Содержание текста", help_text="Введите текст")

    class Meta:
        db_table = "texts"
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"