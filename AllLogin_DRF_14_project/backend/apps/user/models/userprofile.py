from django.db import models

# ----------------------------
# User Profile
# ----------------------------
class UserProfile(models.Model):
    user = models.OneToOneField("user.CustomUser", on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Avatar")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        db_table = "user_profile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"