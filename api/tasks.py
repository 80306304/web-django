from celery import shared_task
import time

from api.function.sendPush import sendMsg


@shared_task
def process_data(data):
    """处理数据的异步任务"""
    time.sleep(5)  # 模拟耗时操作
    result = f"Processed: {data.upper()}"
    return result

@shared_task
def send_notification(token, message):
    """发送通知的异步任务"""
    # 实际应用中这里会连接邮件服务或推送服务
    sendMsg(token,"任务已开启")
    return f"Notification sent to user {user_id}: {message}"
