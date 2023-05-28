from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/<int:chat_id>', ChatConsumer.as_asgi()),
]