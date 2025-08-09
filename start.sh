#!/bin/bash

# 启动Celery Worker（连接外部MQ）
celery -A DjangoProject1 worker --loglevel=info &

# 如需定时任务，启动Celery Beat
# celery -A your_project_name beat --loglevel=info &


# 启动Django服务
python manage.py runserver 0.0.0.0:8000