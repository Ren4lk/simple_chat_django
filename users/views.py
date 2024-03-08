from typing import cast
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import redis

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User
from users.utils import remove_user_online_data, save_user_online_data



def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("chat:index"))

    if not request.session.session_key:
        request.session.create()

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = cast(User, auth.authenticate(username=username, password=password))

            if user:
                auth.login(request, user)
                save_user_online_data(request, user)
                messages.success(request, f"{username} logged in!")
                return HttpResponseRedirect(reverse("chat:index"))
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
        return HttpResponseRedirect(reverse("chat:index"))

    if not request.session.session_key:
        request.session.create()

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            user = cast(User, form.save(commit=False))
            save_user_online_data(request, user)
            auth.login(request, user)
            messages.success(request, f"{user.username} registered and logged in!")
            return HttpResponseRedirect(reverse("chat:index"))
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


# @login_required
# def edit(request: HttpRequest) -> HttpResponse:
#     pass


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)

    remove_user_online_data(user)
    # user.is_online = False
    # user.save()

    auth.logout(request)
    messages.success(request, f"{user.username} logged out!")
    return redirect(reverse("users:login"))
