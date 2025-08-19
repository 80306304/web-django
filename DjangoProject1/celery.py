import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject1.settings')

app = Celery(
    'DjangoProject1',
    # 关键配置：
    broker_heartbeat=30,  # 每 30 秒发送一次心跳包（单位：秒）
    broker_pool_limit=None,  # 禁用连接池（避免连接复用导致的超时）
    result_backend_always_retry=True,  # 结果后端连接失败时重试
    result_backend_retry_policy={
        'max_retries': 10,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    }
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
