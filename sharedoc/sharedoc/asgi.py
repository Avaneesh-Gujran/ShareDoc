"""
ASGI config for sharedoc project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharedoc.settings')

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
  # replace 'myapp' with your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharedoc.settings')  # replace 'myproject' with your project name


application = get_asgi_application()
