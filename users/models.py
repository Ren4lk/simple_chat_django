from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDERS = [
        ("m", "Male"),
        ("f", "Female"),
    ]

    LANGUAGES = [
        ("en", "English"),
        ("ru", "Russian"),
    ]

    ip = models.GenericIPAddressField(blank=True, null=True)

    session_key = models.CharField(max_length=40, blank=True, null=True)

    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True)

    language = models.CharField(max_length=10, choices=LANGUAGES, blank=True, null=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

class OnlineUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = "online_users"
        verbose_name = "Online user"
        verbose_name_plural = "Online users"

    def __str__(self):
        return self.user.username