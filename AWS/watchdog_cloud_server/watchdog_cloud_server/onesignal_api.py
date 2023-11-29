from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import requests

ONESIGNAL_ENDPOINT = 'https://onesignal.com/api/v1/notifications'

## todo: test only
import json
user_ids = []
@csrf_exempt
def register_mobile(request):
    global user_ids
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId', '')
        print(f"user_id: {user_id}")
        if user_id not in user_ids:
            user_ids.append(user_id)
        print(user_ids)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

def send_notification(content,head, notificationId):
    global user_ids
    response = send_notification_by_user_id(user_ids, content, head, notificationId)

    return JsonResponse(response.json(), status=response.status_code)


def send_notification_test(request):
    global user_ids
    response = send_notification_by_user_id(user_ids, 'test111', 'test11111', '101')

    return JsonResponse(response.json(), status=response.status_code)

def send_notification_by_user_id(user_ids, contents, headings, notificationId = ''):
    
    headers = {
        "Authorization": "Basic " + settings.ONESIGNAL['key'],
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": settings.ONESIGNAL['app_id'],
        "include_player_ids": user_ids,
        "existing_android_channel_id": settings.ONESIGNAL['android_channel_id'],
        "contents": {"en": contents},
        "headings": {"en": headings},
        "data": {
            "targetScreen": "Notification",
            'notificationId': notificationId
        },
        "priority": 10
    }

    response = requests.post(ONESIGNAL_ENDPOINT, json=payload, headers=headers)

    return response