import requests
import json


def sendPush(data: dict = {}):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAArIL4nuM:APA91bEJw8psWb0Ym8WSQhV8n5FFaxHT4T3a1U21vMtrVZ2kw23vjzz-wEE7SsgUoIOHJPdrdh0Q-MxS2pRWjh_TiDr6r_vwHhkY5EZMUMh6PpjaziuVG9DOxlM3Ltkb3qENtgViRoqu',
    }
    body = {
        "data": data,
        'to': "/topics/all",
        "priority": "high",
    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    return response.status_code