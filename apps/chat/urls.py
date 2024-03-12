from django.urls import path
from .views import chat_room, ChatViewSet
urlpatterns = [
    path('rooms/', ChatViewSet.as_view({'get': 'list', 'post': 'create_chat'}), name='chat_room'),  # Для списка чатов используется метод GET
    path('room/<int:pk>/', ChatViewSet.as_view({'get': 'retrieve'}), name='room'),
    path('room/update/<int:pk>/', ChatViewSet.as_view({'post': 'update_chat'}), name='room'),

    path('room/<int:room_id>/', chat_room, name='room'),

]

