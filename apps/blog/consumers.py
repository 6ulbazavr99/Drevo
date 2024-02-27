import json
from datetime import datetime

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user

from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_chat_participants_count(self, chat):
        return chat.participants.count()

    @sync_to_async
    def get_chat(self, room_id, user):
        chat, created = Chat.objects.get_or_create(id=room_id)
        if chat.participants.count() < 2:
            chat.participants.add(user)
        return chat

    @sync_to_async
    def create_message(self, chat, user, message):
        message = Message.objects.create(
            chat=chat,
            sender=user,
            content=message
        )

    async def connect(self):
        user = await get_user(self.scope)

        if user.is_authenticated:
            self.room_id = self.scope['url_route']['kwargs']['room_id']

            chat = await self.get_chat(self.room_id, user)
            participants_count = await self.get_chat_participants_count(chat)

            if participants_count > 2:
                await self.close()
                return

            self.room_group_name = f"chat_{self.room_id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        user = await get_user(self.scope)
        data = json.loads(text_data)
        message = data['message']

        chat = await self.get_chat(self.room_id, user)

        await self.create_message(chat, user, message)

        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': user.username,
                'timestamp': formatted_time,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
