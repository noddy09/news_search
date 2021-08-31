import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_bl.settings')

app = Celery('news_bl')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
   result_extended=True
)
app.autodiscover_tasks()