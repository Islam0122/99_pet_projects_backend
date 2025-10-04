from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils.html import strip_tags


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username or email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_active", True)
        return self.create_user(email=email, username=username, password=password, **extra_fields)


class User(AbstractUser):
    fullname = models.CharField(max_length=255, verbose_name="Полное имя")
    is_allowed = models.BooleanField(default=True, verbose_name="Разрешен")

    ROLE_CHOICES = [
        ("cashier", "Кассир"),
        ("admin", "Админ"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cashier")
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def set_random_password_and_notify(self):
        """Генерирует временный пароль, устанавливает его и отправляет email"""
        password = get_random_string(10)
        self.set_password(password)
        self.save()
        self.send_welcome_email(password)

    def send_welcome_email(self, password):
        """Отправляет email пользователю с данными для входа"""
        if not self.email:
            return

        subject = "Добро пожаловать в MINI-POS!"

        html_message = f"""
        <h2>Привет, {self.username}! 👋</h2>

        <p>Мы рады приветствовать вас в системе <b>MINI-POS</b>! 🎉</p>

        <p><b>Ваши данные для входа:</b></p>
        <ul>
            <li><b>Логин:</b> {self.email}</li>
            <li><b>Пароль:</b> {password}</li>
        </ul>

        <p style="color: red;"><b>⚠️ Не передавайте эти данные третьим лицам!</b></p>

        <p>Если возникнут вопросы, мы всегда на связи. 🤝</p>

        <p>С уважением,<br>
        Islam Dev (<a href="mailto:duishobaevislam01@gmail.com">duishobaevislam01@gmail.com</a>) 🚀</p>
        """

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email="duishobaevislam01@gmail.com",
            recipient_list=[self.email],
            html_message=html_message,
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
