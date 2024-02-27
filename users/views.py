from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import transaction

from users.forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse

from users.models import OnlineUser


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("chat:index"))
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

                OnlineUser.objects.create(user=user, session_key=request.session.session_key, ip=request.META["REMOTE_ADDR"])
                
                messages.success(request, f"{username} logged in!")

                return HttpResponseRedirect(reverse("chat:index"))
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
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            OnlineUser.objects.create(user=user, session_key=request.session.session_key, ip=request.META["REMOTE_ADDR"])

            messages.success(request, f"{user.username} registered!")

            return HttpResponseRedirect(reverse("chat:index"))
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
    OnlineUser.objects.filter(user=request.user).delete()
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect(reverse("users:login"))
