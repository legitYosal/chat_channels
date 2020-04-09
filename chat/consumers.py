import json
from .exceptions import ClientError
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import get_user_matches

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # join room group
        # print('connect \n', self.scope['url_route'])
        # async_to_sync(self.channel_layer.group_add)(

        print(f'log:: user: {self.scope["user"].username} has logged in')
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # async_to_sync(self.channel_layer.group_send)(
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        print (f'log: user {self.scope["user"].username} sended something')
        # self.send(text_data=json.dumps({
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatRealConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('log: connect request')
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            print('log: connect accepted')
            await self.accept()

    async def disconnect(self, code):
        print('client disconnected')
        pass

    async def receive(self, text_data):
        content = json.loads(text_data)
        command = content.get('command', None)
        print(content)
        try:
            if command == 'user_search':
                await self.match_user(content['user_name'])

        except ClientError as e:
            await self.send(text_data=json.dumps({'error': e.code}))


    async def match_user(self, user_name):
        matches = await get_user_matches(user_name, self.scope['user'])
        await self.send(text_data=json.dumps({
            'msg_type': 'search_bar_matches',
            'matches' : matches
        }))
