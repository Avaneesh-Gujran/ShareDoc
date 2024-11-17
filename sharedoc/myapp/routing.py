# myapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/edit/<uuid:document_id>/', consumers.DocumentConsumer.as_asgi()),
]
