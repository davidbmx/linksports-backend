# chat/routing.py
from django.urls import re_path

from actions.consumers import ActionsConsumer

websocket_urlpatterns = [
    re_path(r'ws/actions', ActionsConsumer.as_asgi()),
]
