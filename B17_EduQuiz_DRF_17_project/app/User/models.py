from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils.html import strip_tags


class User(AbstractUser):
    fullname = models.CharField(max_length=255, verbose_name="Полное имя")
    is_allowed = models.BooleanField(default=True, verbose_name="Разрешен")

    def set_random_password_and_notify(self):
        """Генерирует временный пароль, устанавливает его и отправляет email"""
        password = get_random_string(10)  # Генерируем случайный пароль из 10 символов
        self.set_password(password)  # Устанавливаем хешированный пароль
        self.save()

        self.send_welcome_email(password)  # Отправляем email пользователю


    def send_welcome_email(self, password):
        """Отправляет email пользователю с данными для входа"""
        if not self.email:
            return  # Если email нет, не отправляем письмо

        subject = 'Добро пожаловать в EduQuiz!'

        html_message = f'''
        <h2>Привет, {self.username}! 👋</h2>

        <p>Мы рады приветствовать вас в системе <b>EduQuiz</b>! 🎉</p>

        <p><b>Ваши данные для входа:</b></p>
        <ul>
            <li><b>Логин:</b> {self.username}</li>
            <li><b>Пароль:</b> {password}</li>
        </ul>

        <p>🔗 <a href="https://t.me/+1zXVUPd6-g9kODQy">Наш канал для получения результатов</a></p>

        <p style="color: red;"><b>⚠️ Не передавайте эти данные третьим лицам!</b></p>

        <p>Если возникнут вопросы, мы всегда на связи. 🤝</p>

        <p>С уважением,<br>
        Duishobaev Islam (<a href="mailto:duishobaevislam01@gmail.com">duishobaevislam01@gmail.com</a>) 🚀</p>
        '''

        plain_message = strip_tags(html_message)  # Удаляем HTML теги для обычной версии

        send_mail(
            subject=subject,
            message=plain_message,  # Обычная версия
            from_email='duishobaevislam01@gmail.com',
            recipient_list=[self.email],
            html_message=html_message  # HTML-версия
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
