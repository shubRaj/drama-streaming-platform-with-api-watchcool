import requests
import json


def sendPush(data: dict = {}):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAagvPTK8:APA91bGspTtDPMV2LuGvJs8mC9aVALBkPEd9WaJn1jhbdhYNaLdtx4sH7MGXzmg8nAWvCLMBLQbD509hGPixa4y_qCnRrhne5E7eAJaAc1l-DguklC5Jh1dYSlb3zla8zmwp7sNRzLEC',
    }
    body = {
        "data": data,
        'to': "/topics/all",
        "priority": "high",
    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    return response.status_code