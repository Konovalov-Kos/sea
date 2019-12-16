from channels.generic.websocket import AsyncWebsocketConsumer
import json

from front.models import Games


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("user: ", self.scope.get('user'))
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("receive--")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        print(self.scope)
        vistrel = self.scope['url_route']['kwargs']['room_name']
        #todo: Проверить
        game = Games.objects.get(pk=text_data_json['game_id'])
        user = self.scope.get('user')
        if game.board1.user_id == user.pk:
            opponent_board = game.board2
        elif game.board2.user_id == user.pk:
            opponent_board = game.board1
        else:
            print("Посторонние в канале!")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        await self.channel_layer.group_send(
            f'chat_{opponent_board.socket_room}',
            {
                'type': 'chat_message',
                'message': message
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))