from celery import shared_task

from api.activity.game1 import get_ad, finish_game

@shared_task
def process_data(gameToken, uuid, pushToken: str = None):
    """处理数据的异步任务"""
    try:
        result = get_ad(gameToken, uuid, pushToken)
        return {"status": "success", "result": result}
    except Exception as e:
        # 可以在这里添加日志记录
        return {"status": "error", "message": str(e)}

@shared_task
def play_game(gameToken, uuid, pushToken: str = None):
    try:
        result = finish_game(gameToken, uuid, pushToken)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}