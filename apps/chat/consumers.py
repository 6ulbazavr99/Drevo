import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.db.models import sync_to_async
from django.db.models.functions import sync_to_async
from apps.chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Присоединение к группе чата
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключение от группы чата
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Обработка сообщений, отправляемых в группу
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]
        room_id = self.room_id

        # Сохранение сообщения в базу данных
        await self.save_message(room_id, user, message)

        # Отправка сообщения всем участникам группы
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def save_message(self, room_id, user, message_text):
        Message.objects.create(
            chat_id=room_id,
            sender=user,
            content=message_text
        )
