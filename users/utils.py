from django.http import HttpRequest
import redis

from users.models import User

# r = redis.Redis(host="localhost", port=6379)


def save_user_online_data(request: HttpRequest, user: User):
    user.ip = request.META["REMOTE_ADDR"]
    user.session_key = request.session.session_key

    user.is_online = True
    # r.sadd("online_users", user.username)
    # print(user.username)

    user.save()


def remove_user_online_data(user: User):
    # r.srem("online_users", user.username)
    user.is_online = False
    user.save()
