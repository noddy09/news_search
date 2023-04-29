import json
from os import name
from .sealirizers import ArticleSerializer
from .models import Article
from channels import layers
from asgiref.sync import async_to_sync
from celery import shared_task
from django.conf import settings

from .models import *

@shared_task
def fetch_news(keyword, channel_name):
    articles_res = None
    try:
        response = settings.NEWSAPI.get_everything(q=keyword)
        print(response)
        articles_res = response.get('articles')
        channel_layer = layers.get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name,
            {
                "type": "websocket.send",
                "text": ("search", articles_res),
            })
        kw, _ = Keyword.objects.get_or_create(name=keyword)
        for article in articles_res:
            source, created = Source.objects.get_or_create(name=article['source']['name'])
            article['source'] = source
            artcl, _ = Article.objects.get_or_create(**article)
            kw.articles.add(artcl)
    except Exception as ex:
        pass
        raise ex
