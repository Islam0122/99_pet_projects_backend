import os
from io import BytesIO
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML
import logging

from .models import ResultsTest

logger = logging.getLogger(__name__)


@shared_task
def generate_certificate_and_send_email(result_id):
    try:
        instance = ResultsTest.objects.get(id=result_id)

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

        # отправляем email
        if instance.email:
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[instance.email],
            )
            email.attach(filename, pdf_content, 'application/pdf')
            email.send()
        else:
            logger.warning(f"Email не указан для ResultsTest {instance.id}")

        pdf_file.close()

        logger.info(f"Сертификат успешно сгенерирован и отправлен для ResultsTest {instance.id}")

    except Exception as e:
        logger.error(f"Ошибка при генерации сертификата или отправке письма: {e}")
