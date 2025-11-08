from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import logging
from weasyprint import HTML
import os
from .placementtest import PlacementTest
from  .basemodel import  BaseModel
from .test import Test
from .level import Level

logger = logging.getLogger(__name__)

# ===========================
# Результат теста + Сертификат
# ===========================
class ResultsTest(BaseModel):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Тест',
        help_text='Выберите тест, который прошёл пользователь'
    )
    name = models.CharField(max_length=255, verbose_name='Имя пользователя', help_text='Имя пользователя для сертификата')
    email = models.EmailField(verbose_name='Email пользователя', help_text='Email для отправки сертификата')
    score = models.PositiveIntegerField(verbose_name='Набранные баллы')
    total_questions = models.PositiveIntegerField(verbose_name='Всего вопросов')
    correct_answers = models.PositiveIntegerField(verbose_name='Правильные ответы')
    wrong_answers = models.PositiveIntegerField(verbose_name='Неправильные ответы')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент правильных ответов')
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True, verbose_name='Сертификат (PDF)')

    def __str__(self):
        return f"Результат '{self.test.name}' — {self.name} ({self.email})"

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        ordering = ['-created_at']




# ===========================
# Результат теста + Сертификат
# ===========================
class PlacementTestResult(BaseModel):
    """Результат прохождения Placement Test"""

    test = models.ForeignKey(
        'PlacementTest',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Тест',
        help_text='Выберите тест, который прошёл пользователь'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя для сертификата'
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        help_text='Email для отправки сертификата'
    )

    # Общие показатели
    total_questions = models.PositiveIntegerField(
        verbose_name='Всего вопросов',
        default=0
    )
    correct_answers = models.PositiveIntegerField(
        verbose_name='Правильные ответы',
        default=0
    )
    wrong_answers = models.PositiveIntegerField(
        verbose_name='Неправильные ответы',
        default=0
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент правильных ответов',
        default=0
    )
    score = models.PositiveIntegerField(
        verbose_name='Набранные баллы',
        default=0
    )

    # Правильные ответы по уровням
    level_a1_correct = models.PositiveIntegerField(default=0)
    level_a2_correct = models.PositiveIntegerField(default=0)
    level_b1_correct = models.PositiveIntegerField(default=0)
    level_b2_correct = models.PositiveIntegerField(default=0)
    level_c1_correct = models.PositiveIntegerField(default=0)
    level_c2_correct = models.PositiveIntegerField(default=0)

    # Определённый уровень
    level = models.ForeignKey(
        'Level',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Определённый уровень",
        help_text="Какой уровень был определён по результатам теста"
    )

    # Сертификат
    certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True,
        verbose_name='Сертификат (PDF)'
    )


    class Meta:
        verbose_name = 'Результат Placement теста'
        verbose_name_plural = 'Результаты Placement тестов'
        ordering = ['-created_at']

    def __str__(self):
        return f"Результат '{self.test.name}' — {self.name} ({self.email})"

    def save(self, *args, **kwargs):
        """Автоматический пересчёт результатов перед сохранением"""
        # Считаем общие правильные ответы
        self.correct_answers = (
                self.level_a1_correct + self.level_a2_correct +
                self.level_b1_correct + self.level_b2_correct +
                self.level_c1_correct + self.level_c2_correct
        )
        self.wrong_answers = self.total_questions - self.correct_answers

        # Взвешенный счёт (для уровня)
        self.score = (
                (self.level_a1_correct * 2) +
                (self.level_a2_correct * 2.5) +
                (self.level_b1_correct * 3) +
                (self.level_b2_correct * 3.5) +
                (self.level_c1_correct * 4) +
                (self.level_c2_correct * 4.5)
        )

        # --- Процент успеха по кол-ву правильных ответов ---
        if self.total_questions > 0:
            self.percentage = round((self.correct_answers / self.total_questions) * 100, 2)
        else:
            self.percentage = 0

        # --- Определение уровня по ВЕСУ (score) ---
        if self.percentage >= 90:
            level_title = "C2"
        elif self.percentage >= 75:
            level_title = "C1"
        elif self.percentage >= 60:
            level_title = "B2"
        elif self.percentage >= 45:
            level_title = "B1"
        elif self.percentage >= 30:
            level_title = "A2"
        else:
            level_title = "A1"

        self.level = Level.objects.filter(title=level_title).first()

        super().save(*args, **kwargs)


# ===========================
# Сигнал: генерация сертификата и отправка на почту
# ===========================

@receiver(post_save, sender=PlacementTestResult)
def generate_certificate_and_send_email2(sender, instance, created, **kwargs):
    if created and not instance.certificate:
        context = {
            'name': instance.name,
            'topic': instance.test.name,
            'level': instance.level.title if instance.level else "Не определён",
            'percentage': instance.percentage,
            'correct_answers': instance.correct_answers,
            'total_questions': instance.total_questions,
            'date': instance.created_at.strftime('%d-%m-%Y'),
        }

        html_string = render_to_string("certificate2_template.html", context)

        pdf_file = BytesIO()
        base_url = f'file://{os.path.join(settings.BASE_DIR, "core", "static")}/'
        HTML(string=html_string, base_url=base_url).write_pdf(pdf_file)

        pdf_file.seek(0)
        filename = f"certificate_{instance.id}.pdf"
        pdf_content = pdf_file.read()
        instance.certificate.save(filename, ContentFile(pdf_content))

        email_subject = '🎓 Ваш сертификат за прохождение теста по английскому'
        email_body = f"""
        Здравствуйте, {instance.name}!

        Поздравляем с завершением теста "{instance.test.name}"! 🎉

        Ваш результат:
        - Определённый уровень: {context['level']}
        - Правильных ответов: {context['correct_answers']}
        - Неправильных ответов: {instance.wrong_answers}
        - Процент правильных ответов: {context['percentage']}%

        Ваш персональный сертификат прикреплён к письму.

        С уважением Islam Dev,  
        Команда обучения английскому 🌟
        """
        try:
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[instance.email],
            )
            email.attach(filename, pdf_content, 'application/pdf')
            email.send()
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {e}")

        pdf_file.close()