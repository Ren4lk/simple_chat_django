from django.urls import path, re_path

from chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<target_user>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path("ws/chat/", consumers.ChatConsumer.as_asgi()),
]
