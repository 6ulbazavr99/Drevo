from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from apps.chat.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r'api/v1/chat/room/(?P<room_id>\d+)/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
