import json
from channels.consumer import SyncConsumer
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync
from celery.result import AsyncResult
import time

from .models import *
from .sealirizers import ArticleSerializer

class NewsAPIConsumer(SyncConsumer):
    def websocket_connect(self, event):
        """
        Receive connection request.
        Making connection with authorized users only.
        """
        try:
            token = Token.objects.select_related('user').get(key=self.scope['query_string'].decode()[5:])
            async_to_sync(self.channel_layer.group_add)(token.user.username, token.user.username)
        except Exception as ex:
            self.send({
                "type": "websocket.close",
            })
        else:
            self.send({
                "type": "websocket.accept",
            })

    def websocket_receive(self, event):
        """
        Receive message from WebSocket.
        Get the events and send corresponding messages.
        """
        try:
            data = json.loads(event['text'])
            if data[0] == "suggest":
                keys = Keyword.objects.filter(name__istarts_with=data[1]).values_list('name', flat=True)
                self.send({
                    "type": "websocket.send",
                    "text": json.dumps(["suggest", keys]),
                })

            elif data[0] == "search":
                task = AsyncResult(data[1])
                counter = 0
                while task.status not in ('SUCCESS', 'FAILURE') and counter < 11:
                    time.sleep(1.5)
                    counter+=1

                if task.status == 'SUCCESS':
                    articles = Article.objects.filter(keyword__name__iexact=task.args[0])
                    data = ArticleSerializer(articles, many=True).data
                    self.send({
                    "type": "websocket.send",
                    "text": json.dumps(["search", task.args[0], data]),
                    })
                else:
                    self.send({
                    "type": "websocket.send",
                    "text": json.dumps(["search", "", []]),
                    })
        except Exception as ex:
            pass

    def websocket_disconnect(self, event):
        print(event)