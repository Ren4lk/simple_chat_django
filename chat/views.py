import re
from urllib import response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from chat.models import Message
from django.core import serializers
from users.models import User
from django.middleware.csrf import rotate_token
from django.middleware.csrf import get_token


# # Create your views here.
# def chat(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("users:login"))

#     contacts = User.objects.all()
#     messages = Message.objects.filter(receiver=request.user)

#     context = {"title": "Chat", "contacts": contacts, "messages": messages}
#     return render(request, "chat/index.html", context)


# def update_contacts(request):
#     contacts = User.objects.all()
#     contacts_list = [{"username": contact.username} for contact in contacts]
#     rotate_token(request)
#     csrf_token = get_token(request)
#     return JsonResponse({"contacts": contacts_list, "csrfmiddlewaretoken": csrf_token})

from django.shortcuts import render
from users.models import User


def index(request, target_user=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    if not User.objects.filter(username=request.user).exists():
        return render(request, "chat/index.html")

    return render(
        request,
        "chat/index.html",
        {"target_user": target_user, "current_user": request.user.username},
    )

    # return render(request, "chat/index_test.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})
