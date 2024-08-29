import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Location
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the user ID from the URL route
        self.room_group_name = 'test'
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        longitude = text_data_json.get('longitude')
        latitude = text_data_json.get('latitude')

        print(longitude, latitude)
        # Save the message to the database
        await self.save_message(longitude, latitude)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'location',
                'latitude': latitude,
                'longitude': longitude
            }
        )

    async def location(self, event):
        longitude = event['longitude']
        latitude = event['latitude']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location',
            'longitude': longitude,
            'latitude': latitude
        }))

    @database_sync_to_async
    def save_message(self, longitude: float, latitude: float):
        try:
            Location.objects.create(longitude=longitude, latitude=latitude)
        except Location.DoesNotExist:
            # Handle the case where the user does not exist
            pass
