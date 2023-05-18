# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 获取url中的房间名参数
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 通过房间名创建一个channels组
        self.room_group_name = 'chat_%s' % self.room_name

        # 加入这个组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # 接受socket连接
        await self.accept()

    async def disconnect(self, close_code):
        # 离开这个组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 接收来自socket的消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 发送消息到这个组
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 接收来自组的消息
    async def chat_message(self, event):
        message = event['message']

        # 发送消息到socket
        await self.send(text_data=json.dumps({
            'message': message
        }))