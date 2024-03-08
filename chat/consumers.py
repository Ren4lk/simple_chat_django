# chat/consumers.py
import json

# import redis.asyncio as aredis
from channels.generic.websocket import AsyncWebsocketConsumer
from channels_redis.core import RedisChannelLayer
from typing import cast
import redis



import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from users.models import User
from chat.models import Message, get_user_messages

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = cast(User, self.scope["user"])

        if not self.user.is_authenticated:
            await self.close()
            return

        self.online_list_group_name = "all"
        self.target_user = self.scope["url_route"]["kwargs"].get("target_user")
        self.channel_layer = cast(RedisChannelLayer, self.channel_layer)
        self.r = redis.Redis(host="localhost", port=6379)

        # print("connected", self.user.username)

        await self.accept()

        await self.channel_layer.group_add(
            self.online_list_group_name, self.channel_name
        )

        await self.send(
            json.dumps(
                {
                    "type": "users_list",
                    "usernames": [
                        username.decode()
                        for username in await database_sync_to_async(self.r.smembers)(
                            "online_users"
                        )
                    ],
                }
            )
        )

        await self.channel_layer.group_send(
            self.online_list_group_name,
            {"type": "user_joined", "username": self.user.username},
        )

        self.r.sadd("online_users", self.user.username)

        self.user_inbox = f"inbox_{self.user.username}"

        print(f"user: {self.user.username}, user_inbox: {self.user_inbox}") ###############

        await self.channel_layer.group_add(self.user_inbox, self.channel_name)

        await self.send(
            json.dumps(
                {
                    "type": "messages_list",
                    "messages": await database_sync_to_async(get_user_messages)(
                        self.user
                    )
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.online_list_group_name,
            {"type": "user_left", "username": self.user.username},
        )

        await self.channel_layer.group_discard(
            self.online_list_group_name, self.channel_name
        )

        self.r.srem("online_users", self.user.username)

        await self.channel_layer.group_discard(self.user_inbox, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)  # type: ignore
        message = text_data_json["message"]


        print(f"Recieve, user: {self.user.username}, target: {self.target_user}, message: {message}")

        receiver = await database_sync_to_async(User.objects.get)(username=self.target_user)

        await database_sync_to_async(Message.objects.create)(
            sender=self.user, receiver=receiver, text=message
        )

        await self.channel_layer.group_send(
            f"inbox_{self.target_user}", {"type": "chat_message", "message": message}
        )

        await self.send(json.dumps({
            "type": "chat_message_delivered",
            "message": message}))



    async def messages_list(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    # async def chat_message_delivered(self, event):
    #     print(event)
    #     await self.send(text_data=json.dumps(event))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_left(self, event):
        await self.send(text_data=json.dumps(event))
