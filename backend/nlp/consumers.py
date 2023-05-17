from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SpeechConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Print the received text_data
        data = json.loads(text_data)
        words = data.get('words')
        print("frontend:", words)
        
        if words:
            await self.send_message(words)

    async def send_message(self, message):
        # Send a message to the WebSocket connection
        await self.send(json.dumps({
            'message': message
        }))