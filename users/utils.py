from django.http import HttpRequest

from users.models import User


def save_user_data(request: HttpRequest, user: User):
    user.ip = request.META["REMOTE_ADDR"]
    user.session_key = request.session.session_key
    user.save()
