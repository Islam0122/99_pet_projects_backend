from django.db import models
import logging
from .basemodel import BaseModel
from .test import Test
logger = logging.getLogger(__name__)

# ===========================
# Вопрос (Question)
# ===========================
class Question(BaseModel):
    QUESTION_TYPES = [
        ("mcq", "Multiple Choice"),
        ("fill", "Fill in the blank"),
        ("translate", "Translate"),
        ("listening", "Listening"),
    ]

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест",
        help_text="Выберите тест, к которому относится вопрос"
    )
    text = models.TextField(
        verbose_name="Текст вопроса",
        help_text="Сам текст вопроса, который увидит пользователь"
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default="mcq",
        verbose_name="Тип вопроса",
        help_text="Выберите тип вопроса"
    )

    # Multiple Choice варианты
    option_a = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант A")
    option_b = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант B")
    option_c = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант C")
    option_d = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вариант D")

    correct_answer = models.TextField(
        verbose_name="Правильный ответ",
        help_text="Для MCQ укажите букву A/B/C/D, для других типов — правильный текст"
    )
    translation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Перевод / подсказка",
        help_text="Подсказка или перевод для вопросов на перевод"
    )

    # Медиа
    image = models.ImageField(
        upload_to="questions_images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="При необходимости добавьте изображение к вопросу"
    )
    audio_file = models.FileField(
        upload_to="questions_audio/",
        blank=True,
        null=True,
        verbose_name="Аудио файл",
        help_text="При необходимости добавьте аудио для вопросов типа Listening"
    )

    def is_correct(self, answer: str) -> bool:
        """Проверяет правильность ответа"""
        if self.question_type == "mcq":
            return self.correct_answer.upper() == answer.upper()
        else:
            return self.correct_answer.strip().lower() == answer.strip().lower()

    def __str__(self):
        return f"{self.text[:50]}..."

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['test', 'id']
