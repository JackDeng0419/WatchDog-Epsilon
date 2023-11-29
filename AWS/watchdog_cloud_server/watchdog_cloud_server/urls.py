"""watchdog_cloud_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from . import views
from . import onesignal_api

def home(request):
    return JsonResponse({"message": "Welcome to my site!"})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    path('log/create/', views.create_log),

    path('patient/setting/create/', views.create_patient_setting),
    path('patient/list/', views.get_patient_list),
    path('patient/create/', views.create_patient),
    path('patient/<patient_id>/', views.get_patient_by_id), # must be  at last

    path('video/upload/', views.upload_video),
    path('video/download/<file_id>/', views.download_video),
    
    path('mqtt/push/', views.publish_mqtt_message),

    path('mobile/register/', onesignal_api.register_mobile),

    path('notification/create/', views.create_notification),
    path('notification/list/', views.get_notification_list),
    path('notification/update/', views.update_notification),
    path('notification/test/',onesignal_api.send_notification_test), # test only
    path('notification/<str:notificationId>/',views.get_notification_by_id),  # must be  at last

    path('room/create/', views.create_room),
    path('room/list/', views.list_rooms),
    path('room/update/<str:room_id>/', views.update_room),
    path('room/delete/<str:room_id>/', views.delete_room),

    path('bed/create/', views.create_bed),
    path('bed/update/<str:bed_id>/', views.update_bed),
    path('bed/delete/<str:bed_id>/', views.delete_bed),
    path('bed/list/', views.list_beds),

    path('user/create/', views.create_user),
    path('user/login/', views.login_user),
    path('user/register/', views.register_user),
    path('user/logout/', views.logout_user),

    path('sensor/register/',views.register_sensor),
]
