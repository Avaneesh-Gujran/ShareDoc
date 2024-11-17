# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DocumentEditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Capture the document ID from the URL route
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        print(f"Attempting to connect WebSocket for document ID: {self.document_id}")

        # Join a group specific to the document (for multi-user editing)
        await self.channel_layer.group_add(
            self.document_id,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()
        print(f"WebSocket connection established for document ID: {self.document_id}")

    async def disconnect(self, close_code):
        # Leave the group on disconnection
        print(f"WebSocket connection closed with code: {close_code} for document ID: {self.document_id}")
        await self.channel_layer.group_discard(
            self.document_id,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received message: {text_data} for document ID: {self.document_id}")
        data = json.loads(text_data)
        content = data.get('content', '')

        # Echo the message back to the client for testing purposes
        await self.send(text_data=json.dumps({'content': content}))
        print(f"Sent back content: {content}")
