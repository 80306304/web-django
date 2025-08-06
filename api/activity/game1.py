import time
import requests
from api.function.sendPush import sendMsg


def get_ad(token,uuid,pushToken:str=None):
    if pushToken:
        sendMsg(pushToken, "任务开始通知", "广告任务已开始")
    while True:
        time.sleep(1)
        url = f"https://game.xywzzj.com/gm1/kind11/xiadan?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"kid":"actBox","hdcid":"1","dc":"1"}

        res = requests.post(url, headers=headers, json=data)
        order11Id = res.json().get("order11Id")
        print(res.json())
        url= f"https://game.xywzzj.com/gm1/kind11/success?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        data = {"order11Id":order11Id}
        res = requests.post(url, headers=headers, json=data).json()
        print(res.get("win").get("msg")!="请勿重复点击")
        if res.get("type") == 0 and res.get("win").get("msg")!="请勿重复点击":
            print("广告已看完")
            if pushToken:
                sendMsg(pushToken, "任务完成通知","广告任务已完成")
            return "success"
            break;
        else:
            print("正在看广告")