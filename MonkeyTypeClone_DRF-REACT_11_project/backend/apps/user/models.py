from django.db import models
from django.contrib.auth.models import AbstractUser

AUTH_CHOICES = (
    ('local', 'Local'),
    ('google', 'Google'),
)


class User(AbstractUser):
    """
    Пользователь MonkeyType Clone
    """
    email = models.EmailField(unique=True)
    auth_type = models.CharField(max_length=10, choices=AUTH_CHOICES, default='local')

    best_wpm = models.FloatField(default=0.0, verbose_name="Best Words Per Minute")
    average_accuracy = models.FloatField(default=0.0, verbose_name="Average Accuracy %")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
