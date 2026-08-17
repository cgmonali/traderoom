import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from rooms.models import Room
from .models import Message
from .tasks import analyze_message


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def check_membership(self, user, room_id):

        return RoomMember.objects.filter(
            room_id=room_id,
            user=user,
        ).exists()

    async def connect(self):

        self.room_id = self.scope[
            "url_route"
        ]["kwargs"]["room_id"]

        self.group_name = f"room_{self.room_id}"

        user = self.scope.get("user")

        if user is None or not user.is_authenticated:
            await self.close()
            return

        is_member = await self.check_membership(
            user,
            self.room_id,
        )

        if not is_member:
            await self.close(code=4003)
            return

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

        content = data.get("message")

        if not content:
            await self.send(
                text_data=json.dumps({
                    "error": "Message cannot be empty."
                })
            )
            return

        user = self.scope["user"]

        saved_message = await self.save_message(
            user,
            content,
        )

        analyze_message.delay(
            saved_message["id"]
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
            text_data=json.dumps({
                "message": event["message"],
                "username": event["username"],
                "created_at": event["created_at"],
            })
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
            "id": msg.id,
            "content": msg.content,
            "username": msg.user.username,
            "created_at": msg.created_at.isoformat(),
        }