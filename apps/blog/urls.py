from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.blog import views
from apps.blog.views import ChatListAPIView, ChatDetailAPIView, chat_room

router = SimpleRouter()
router.register('', views.PostViewSet)


urlpatterns = ([
    path('', ChatListAPIView.as_view(), name='chats'),
    path('room/<int:pk>/', ChatDetailAPIView.as_view(), name='chat_room'),
    path('<int:room_id>/', chat_room, name='room'),
])
urlpatterns += router.urls
