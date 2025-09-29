from .basemodel import BaseModel
from .level import Level
from django.db import models


class PlacementTest(BaseModel):
    """Тест для определения уровня"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название теста")
    description = models.TextField(blank=True, null=True, verbose_name="Описание теста")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Placement Test"
        verbose_name_plural = "Placement Tests"


class PlacementTest_Question(BaseModel):
    QUESTION_TYPES = [
        ("mcq", "Multiple Choice"),
        ("fill", "Fill in the blank"),
        ("translate", "Translate"),
        ("listening", "Listening"),
    ]

    test = models.ForeignKey(
        PlacementTest,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест"
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Уровень вопроса",
        help_text="К какому уровню относится вопрос (например, A2)"
    )
    text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="mcq")

    option_a = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант A")
    option_b = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант B")
    option_c = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант C")
    option_d = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант D")

    correct_answer = models.TextField(verbose_name="Правильный ответ")

    image = models.ImageField(upload_to="questions_images/", blank=True, null=True)
    audio_file = models.FileField(upload_to="questions_audio/", blank=True, null=True)

    def __str__(self):
        return f"{self.text[:50]}..."

    class Meta:
        verbose_name = "Placement Test Вопрос"
        verbose_name_plural = "Placement Test Вопросы"