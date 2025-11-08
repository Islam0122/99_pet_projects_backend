from django.db import models

class OTP(models.Model):
    email = models.EmailField(verbose_name="Email пользователя")
    code = models.CharField(max_length=6, verbose_name="OTP код")

    def __str__(self):
        return f"OTP для {self.email}"