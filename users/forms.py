from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)

from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "age", "gender", "language")

    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    age = forms.IntegerField(initial=18)
    gender = forms.ChoiceField(choices=User.GENDERS)
    language = forms.ChoiceField(choices=User.LANGUAGES)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField()
    password = forms.CharField()


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "age", "gender", "language")

    username = forms.CharField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=User.GENDERS)
    language = forms.ChoiceField(choices=User.LANGUAGES)
