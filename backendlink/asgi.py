"""
ASGI config for backendlink project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from actions.routing import websocket_urlpatterns
from actions.authentication import FirebaseMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendlink.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": AllowedHostsOriginValidator(
            FirebaseMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)