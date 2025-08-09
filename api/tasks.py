from celery import shared_task
import time

from api.activity.game1 import get_ad, finish_game
from api.function.sendPush import sendMsg


@shared_task
def process_data(gameToken,uuid,pushToken:str=None):
    """处理数据的异步任务"""
    result = get_ad(gameToken,uuid,pushToken)
    return result

@shared_task
def play_game(gameToken,uuid,pushToken:str=None):
    return finish_game(gameToken,uuid,pushToken)

@shared_task
def send_notification(token):
    """发送通知的异步任务"""
    # 实际应用中这里会连接邮件服务或推送服务

    return sendMsg(token,"任务状态","任务已开始运行")
