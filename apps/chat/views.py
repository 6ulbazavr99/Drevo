from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Chat
from .permissions import IsChatParticipant
from .serializers import ChatSerializer, ChatDetailSerializer, ChatCreateSerializer


User = get_user_model()


class ChatViewSet(mixins.ListModelMixin, GenericViewSet):

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated:
            return Chat.objects.filter(participants=user)
        return Chat.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSerializer
        return ChatCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'create_chat'):
            return [permissions.IsAuthenticated()]
        return [IsChatParticipant()]

    @action(methods=['get'], detail=True)
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Chat, pk=self.kwargs['pk'])

        # Проверяем, принадлежит ли текущий пользователь к участникам чата
        if request.user in instance.participants.all():
            serializer = ChatDetailSerializer(instance)
            return Response(serializer.data, status=201)
        else:
            return Response({"message": "You are not a participant of this chat."},
                            status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=False)
    def create_chat(self, request, *args, **kwargs):
        user = self.request.user

        participants = self.request.data.get('participants')
        chat = Chat.objects.create()
        chat.participants.add(user)
        if participants:
            for participant in set(participants):
                chat.participants.add(participant)
            chat.save()
            serializer = ChatDetailSerializer(chat)
            return Response(serializer.data, status=201)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Participants required'})

    @action(methods=['post'], detail=True)
    def update_chat(self, request, *args, **kwargs):
        try:
            chat_id = kwargs.get('pk')
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            raise NotFound(detail="Чат не найден.")

        user = request.user

        # Проверяем, является ли пользователь участником чата
        if not chat.participants.filter(pk=user.pk).exists():
            raise PermissionDenied(detail="Вы не являетесь участником этого чата.")

        participants = request.data.get('participants', [])
        if participants:
            # Валидация и добавление участников
            existing_users = User.objects.filter(pk__in=set(participants))
            chat.participants.add(*existing_users)

        chat.save()
        serializer = ChatDetailSerializer(chat, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


def chat_room(request, room_id):
    return render(request, 'chat_room.html', {'room_id': room_id})
