from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from app.quiz.models import Topic
from django.core.mail import EmailMessage
from django.conf import settings
import logging
from weasyprint import HTML
import os

logger = logging.getLogger(__name__)


class ResultsTest(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='tests', verbose_name='Тема')
    name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='Email пользователя')
    score = models.PositiveIntegerField(verbose_name='Набранные баллы')
    total_questions = models.PositiveIntegerField(verbose_name='Всего вопросов')
    correct_answers = models.PositiveIntegerField(verbose_name='Правильные ответы')
    wrong_answers = models.PositiveIntegerField(verbose_name='Неправильные ответы')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент правильных ответов')
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True, verbose_name='Сертификат (PDF)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')

    def __str__(self):
        return f"Тест по теме '{self.topic.name}' от {self.name} ({self.email})"

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        ordering = ['-created_at']


@receiver(post_save, sender=ResultsTest)
def generate_certificate_and_send_email(sender, instance, created, **kwargs):
    if created and not instance.certificate:
        context = {
            'name': instance.name,
            'topic': instance.topic.name,
            'percentage': instance.percentage,
            'correct_answers': instance.correct_answers,
            'total_questions': instance.total_questions,
            'date': instance.created_at.strftime('%d-%m-%Y'),
        }

        # Рендеринг HTML
        html_string = render_to_string('certificate_template.html', context)

        # Генерация PDF с помощью WeasyPrint
        pdf_file = BytesIO()
        base_url = f'file://{os.path.join(settings.BASE_DIR, "core", "static")}/'
        HTML(string=html_string, base_url=base_url).write_pdf(pdf_file)

        pdf_file.seek(0)
        filename = f"certificate_{instance.id}.pdf"
        pdf_content = pdf_file.read()
        instance.certificate.save(filename, ContentFile(pdf_content))

        # Отправка письма
        email_subject = 'Ваш сертификат за прохождение теста'
        email_body = f"""
        Здравствуйте, {instance.name}!

        Поздравляем вас с успешным завершением теста по теме "{instance.topic.name}"! 🎉

        Мы рады сообщить, что ваш сертификат готов и прикреплен к этому письму. Вы можете скачать его, нажав на файл.

        Ваши результаты:
        - Правильных ответов: {instance.correct_answers}
        - Неправильных ответов: {instance.wrong_answers}
        - Процент правильных ответов: {instance.percentage}%

        Если у вас возникнут вопросы, не стесняйтесь обращаться к нам.

        С наилучшими пожеланиями,
        Ислам Дуйшобаев(duishobaevislam01@gmail.com)
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