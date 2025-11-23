from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, validate_email
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Валидатор для номера телефона
phone_regex = RegexValidator(
    regex=r"^\+?\d{11,15}$",
    message="Номер телефона должен содержать от 11 до 15 цифр."
)


# Менеджер пользователя
class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.
    Позволяет создавать обычных и суперпользователей.
    """
    def create_user(self, phone_number, email=None, password=None):
        if not phone_number:
            raise ValueError("У пользователя должен быть номер телефона.")
        email = self.normalize_email(email) if email else None
        user = self.model(phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, password=None):
        user = self.create_user(phone_number=phone_number, email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[phone_regex],
        verbose_name="Номер телефона",
        db_index=True
    )
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email],
        verbose_name="Электронная почта"
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    user_registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]
    otp = models.CharField(max_length=4, null=True, blank=True)  # Разрешаем null
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.IntegerField(default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    objects = UserManager()

    def __str__(self):
        return self.phone_number


# Профиль пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Пользователь"
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        default="Не указано"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        default="Не указано"
    )
    subscriptions = models.BooleanField(
        default=False,
        verbose_name="Подписка на предложения и акции"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создаёт профиль для нового пользователя.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль пользователя при сохранении пользователя.
    """
    instance.profile.save()
