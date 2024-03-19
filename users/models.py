from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDERS = [
        ("m", "Male"),
        ("f", "Female"),
    ]

    LANGUAGES = [
        ("en", "English"),
        ("ru", "Russian"),
    ]

    ip = models.GenericIPAddressField(editable=False, null=True)
    session_key = models.CharField(max_length=40, editable=False, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, default="m", null=True)
    language = models.CharField(
        max_length=10, choices=LANGUAGES, default="ru", null=True
    )

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
