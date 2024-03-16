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


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "age", "gender", "language")
