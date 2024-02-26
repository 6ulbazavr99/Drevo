from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.blog import permissions
from apps.chat.serializers import ChatDetailSerializer
from apps.chat.models import Chat
from apps.chat.serializers import ChatSerializer


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants=user)


class ChatDetailAPIView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants=user)

    def get_object(self):
        room_id = self.kwargs['pk']
        chat, created = Chat.objects.get_or_create(id=room_id)
        if chat.participants.count() > 2:
            return Response({'error': 'Too many participants in the chat.'}, status=status.HTTP_400_BAD_REQUEST)
        return chat


def chat_room(request, room_id):
    return render(request, 'chat_room.html', {'room_id': room_id})
