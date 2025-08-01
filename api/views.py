# myapp/views.py
from django.http import JsonResponse
from .tasks import process_data,send_notification

class trigger_task:
    def post(self,request):
        task1 = process_data.delay("hello world")
        task2 = send_notification.delay(123, "Welcome!")

        return JsonResponse({
            "task1_id": task1.id,
            "task2_id": task2.id,
            "message": "Tasks submitted successfully"
        })
# def trigger_task(request):
#     # 调用异步任务，任务会被发送到RabbitMQ队列
#     task1 = process_data.delay("hello world")
#     task2 = send_notification.delay(123, "Welcome!")
#
#     return JsonResponse({
#         "task1_id": task1.id,
#         "task2_id": task2.id,
#         "message": "Tasks submitted successfully"
#     })
