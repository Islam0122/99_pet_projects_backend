from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# ----------------------------
# Custom User
# ----------------------------
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, verbose_name="Full Name")
    language = models.CharField(max_length=10, default="ru", verbose_name="Language")
    login_with = models.CharField(
        max_length=20,
        choices=[
            ("github", _("github")),
            ("facebook", _("facebook")),
            ("web browser", _("web browser")),
            ("google", _("google")),
        ],
        default="web_browser",
        verbose_name="Login Method"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Verified Account")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"