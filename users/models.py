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

    ip = models.GenericIPAddressField(editable=False)
    session_key = models.CharField(max_length=40, editable=False)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDERS, default="m")
    language = models.CharField(max_length=10, choices=LANGUAGES, default="ru")

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
