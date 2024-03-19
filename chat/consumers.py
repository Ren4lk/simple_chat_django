import asyncio
import json
import time
from typing import cast

from django.conf import settings
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels_redis.core import RedisChannelLayer
import redis

from chat.models import Message, get_user_messages
from users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    ONLINE_USERS = "online_users"
    USER_DATA = "user_data:{}"
    INBOX = "inbox_{}"
    PING_TIMEOUT = 40
    PING_CHECK_INTERVAL = 5

    async def connect(self):
        self.user = cast(User, self.scope["user"])
        self.last_ping = time.time()

        if not self.user.is_authenticated:
            await self.close()
            return

        self.online_group_name = "all"
        self.channel_layer = cast(RedisChannelLayer, self.channel_layer)
        try:
            self.redis_conn = redis.Redis(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
            )
        except redis.RedisError as e:
            print(f"Redis connection error: {e}")
            await self.close()
            return

        await self.accept()

        await self.add_user_to_group(self.online_group_name)

        online_users = await self.get_online_users()

        await self.send_users_list(online_users)

        await self.send_user_joined()

        await self.add_user_to_online_users()

        self.user_inbox = self.INBOX.format(self.user.username)

        await self.add_user_to_group(self.user_inbox)

        messages = await database_sync_to_async(get_user_messages)(self.user)

        await self.send_messages_list(messages)

        asyncio.create_task(self.check_ping())

    async def disconnect(self, close_code):
        await self.remove_user_from_group(self.user_inbox)

        await self.send_user_left()

        await self.remove_user_from_group(self.online_group_name)

        await self.remove_user_from_online_users()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            if text_data_json.get("type") == "ping":
                self.last_ping = time.time()
                return

            message = text_data_json.get("message")
            target_user = text_data_json.get("target_user")
            if message is None or target_user is None:
                print("Unexpected error: Message or target user is None")
                return

            receiver = await self.get_user(target_user)

            saved_message = await self.save_message(receiver, message)

            await self.send_chat_message(saved_message, target_user)

            await self.send_chat_message_delivered(saved_message)

    async def check_ping(self):
        while self.last_ping - time.time() < self.PING_TIMEOUT:
            await asyncio.sleep(self.PING_CHECK_INTERVAL)
        await self.close()

    async def get_user(self, username):
        try:
            return await database_sync_to_async(User.objects.get)(username=username)
        except User.DoesNotExist as e:
            print(f"Database error in get_user: {e}")
            return None

    async def get_online_users(self):
        try:
            online_usernames = [
                username.decode("utf-8")
                for username in await database_sync_to_async(self.redis_conn.smembers)(
                    self.ONLINE_USERS
                )
            ]
            users = []
            for username in online_usernames:
                user_data = await database_sync_to_async(self.redis_conn.hgetall)(
                    self.USER_DATA.format(username)
                )
                users.append(
                    {k.decode("utf-8"): v.decode("utf-8") for k, v in user_data.items()}
                )
        except redis.RedisError as e:
            print(f"Redis error in get_online_users: {e}")
            return []
        return users

    async def add_user_to_online_users(self):
        try:
            await database_sync_to_async(self.redis_conn.sadd)(
                self.ONLINE_USERS, self.user.username
            )
            await database_sync_to_async(self.redis_conn.hset)(
                self.USER_DATA.format(self.user.username),
                "username",
                self.user.username,
            )
            await database_sync_to_async(self.redis_conn.hset)(
                self.USER_DATA.format(self.user.username), "gender", self.user.gender
            )
            await database_sync_to_async(self.redis_conn.hset)(
                self.USER_DATA.format(self.user.username),
                "language",
                self.user.language,
            )
            print(f"User {self.user.username} has entered the chat!")
        except redis.RedisError as e:
            print(f"Redis error in add_user_to_online_users: {e}")

    async def remove_user_from_online_users(self):
        try:
            await database_sync_to_async(self.redis_conn.srem)(
                self.ONLINE_USERS, self.user.username
            )
            await database_sync_to_async(self.redis_conn.delete)(
                self.USER_DATA.format(self.user.username)
            )
            print(f"User {self.user.username} has left the chat!")
        except redis.RedisError as e:
            print(f"Redis error in remove_user_from_online_users: {e}")

    async def add_user_to_group(self, group_name):
        await self.channel_layer.group_add(group_name, self.channel_name)

    async def remove_user_from_group(self, group_name):
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def save_message(self, receiver, message):
        try:
            return await database_sync_to_async(Message.objects.create)(
                sender=self.user, receiver=receiver, text=message
            )
        except Exception as e:
            print(f"Unexpected exception in save_message: {e}")

    async def send_users_list(self, users):
        await self.send(
            json.dumps(
                {
                    "type": "users_list",
                    "users": users,
                }
            )
        )

    async def send_messages_list(self, messages):
        await self.send(
            json.dumps(
                {
                    "type": "messages_list",
                    "messages": messages,
                }
            )
        )

    async def send_user_joined(self):
        await self.channel_layer.group_send(
            self.online_group_name,
            {
                "type": "user_joined",
                "user": {
                    "username": self.user.username,
                    "gender": self.user.gender,
                    "language": self.user.language,
                },
            },
        )

    async def send_user_left(self):
        await self.channel_layer.group_send(
            self.online_group_name,
            {
                "type": "user_left",
                "user": {
                    "username": self.user.username,
                    "gender": self.user.gender,
                    "language": self.user.language,
                },
            },
        )

    async def send_chat_message(self, created_message, target_user):
        await self.channel_layer.group_send(
            self.INBOX.format(target_user),
            {"type": "chat_message", "message": created_message.to_dict()},
        )

    async def send_chat_message_delivered(self, created_message):
        await self.send(
            json.dumps(
                {"type": "chat_message_delivered", "message": created_message.to_dict()}
            )
        )

    async def messages_list(self, event):
        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_left(self, event):
        await self.send(text_data=json.dumps(event))
