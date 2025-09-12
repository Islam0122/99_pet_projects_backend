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
from  .basemodel import  BaseModel
from .test import Test

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
# Сигнал для генерации сертификата и отправки письма
# ===========================
@receiver(post_save, sender=ResultsTest)
def generate_certificate_and_send_email(sender, instance, created, **kwargs):
    if created and not instance.certificate:
        context = {
            'name': instance.name,
            'topic': instance.test.name,
            'level': instance.test.level,
            'percentage': instance.percentage,
            'correct_answers': instance.correct_answers,
            'total_questions': instance.total_questions,
            'date': instance.created_at.strftime('%d-%m-%Y'),
        }

        html_string = render_to_string("certificate_template.html", context)

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

Поздравляем с успешным завершением теста по теме "{instance.test.name}" ({instance.test.level})! 🎉

Результаты:
- Правильных ответов: {instance.correct_answers}
- Неправильных ответов: {instance.wrong_answers}
- Процент правильных ответов: {instance.percentage}%

Ваш сертификат прикреплён к письму. Скачайте его и сохраняйте!

С уважением,
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
