import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject1.settings')

app = Celery('DjangoProject1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
BROKER_HEARTBEAT = 600  # 心跳间隔60秒
BROKER_CONNECTION_TIMEOUT = 30  # 连接超时30秒
BROKER_CONNECTION_RETRY = True  # 自动重试连接
BROKER_CONNECTION_MAX_RETRIES = 1000  # 最大重试次数