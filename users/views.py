from typing import cast
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from users.forms import UserEditForm, UserLoginForm, UserRegistrationForm
from users.models import User
from users.utils import save_user_data


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("chat:index")

    if not request.session.session_key:
        request.session.create()

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = cast(User, auth.authenticate(username=username, password=password))

            if user is not None:
                auth.login(request, user)
                save_user_data(request, user)
                messages.success(request, f"{username} logged in!")
                return redirect("chat:index")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(
                request, "An error with the form has occurred, check your input!"
            )
    else:
        form = UserLoginForm()

    context = {
        "title": "Login",
        "form": form,
    }
    return render(request=request, template_name="users/login.html", context=context)


def registration(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("chat:index")

    if not request.session.session_key:
        request.session.create()

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            save_user_data(request, user)
            auth.login(request, user)
            messages.success(request, f"{user.username} registered and logged in!")
            return redirect("chat:index")
        else:
            messages.error(
                request, "An error with the form has occurred, check your input!"
            )
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Registration",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserEditForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("users:edit")
        else:
            messages.error(
                request, "An error with the form has occurred, check your input!"
            )
    else:
        form = UserEditForm(instance=request.user)

    context = {
        "title": "Edit Profile",
        "form": form,
    }
    return render(request, "users/edit.html", context)


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    auth.logout(request)
    messages.success(request, f"{user.username} logged out!")
    return redirect("users:login")
