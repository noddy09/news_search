from django.urls import path
from .consumer import NewsAPIConsumer

websocket_urlpatterns = [
    path('ws/newsapi/', NewsAPIConsumer.as_asgi()),
]