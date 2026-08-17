import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from rooms.models import Room
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        self.group_name = f"room_{self.room_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data["message"]

        user = self.scope["user"]

        saved_message = await self.save_message(
            user,
            message,
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": saved_message["content"],
                "username": saved_message["username"],
                "created_at": saved_message["created_at"],
            },
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "created_at": event["created_at"],
                }
            )
        )

    @sync_to_async
    def save_message(self, user, content):

        room = Room.objects.get(
            id=self.room_id
        )

        msg = Message.objects.create(
            room=room,
            user=user,
            content=content,
        )

        return {
            "content": msg.content,
            "username": msg.user.username,
            "created_at": msg.created_at.isoformat(),
        }