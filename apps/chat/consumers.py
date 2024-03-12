import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Chat, Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Проверка на аутентификацию и участие в чате
        if self.scope["user"].is_authenticated and await self.is_chat_participant(self.room_name, self.scope["user"]):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Загрузка истории чата и отправка её пользователю
            messages = await self.get_chat_history(self.room_name)
            for message in messages:
                await self.send(text_data=json.dumps({
                    'message': message['content'],
                    'sender': message['sender_id'],
                    'timestamp': message['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Сохраняем сообщение в базе данных
        await self.save_message(self.scope["user"], self.room_name, message)

        # Отправляем сообщение всем участникам группы
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Отправляем сообщение обратно в WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def is_chat_participant(self, room_id, user):
        try:
            chat = Chat.objects.get(id=room_id)
            return chat.participants.filter(id=user.id).exists()
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, room_id, message):
        chat = Chat.objects.get(id=room_id)
        Message.objects.create(
            chat=chat,
            sender=user,
            content=message,
        )

    @database_sync_to_async
    def get_chat_history(self, room_id):
        chat = Chat.objects.get(id=room_id)
        messages = Message.objects.filter(chat=chat).order_by('timestamp').values('sender_id', 'content', 'timestamp')
        return list(messages)
