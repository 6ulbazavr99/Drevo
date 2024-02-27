from django.urls import path

from apps.chat.views import ChatListAPIView, ChatDetailAPIView, chat_room

urlpatterns = [
    path('', ChatListAPIView.as_view(), name='chats'),
    path('room/<int:pk>/', ChatDetailAPIView.as_view(), name='chat_room'),
    path('<int:room_id>/', chat_room, name='room'),
]
