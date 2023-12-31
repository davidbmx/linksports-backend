import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ActionsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if user.is_authenticated:
            self.user_channel = f'user_{user.uid}'
            self.actions_channel = 'user_actions'
            await self.channel_layer.group_add(self.user_channel, self.channel_name)
            await self.channel_layer.group_add(self.actions_channel, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user.is_authenticated:
            await self.channel_layer.group_discard(self.user_channel, self.channel_name)
            await self.channel_layer.group_discard(self.actions_channel, self.channel_name)

    async def receive(self, text_data):
        pass

    async def handle_actions(self, data):
        await self.send(data['action'])