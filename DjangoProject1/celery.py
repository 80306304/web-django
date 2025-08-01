# myproject/celery.py
import os
from celery import Celery

# 设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject1.settings')

# 创建 Celery 实例
app = Celery('api')

# 从 Django settings 中读取配置（以 CELERY_ 为前缀的配置）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有应用中的 tasks.py（任务文件）
app.autodiscover_tasks()
