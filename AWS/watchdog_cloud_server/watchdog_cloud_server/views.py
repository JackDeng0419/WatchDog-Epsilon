from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from gridfs import GridFS
from gridfs.errors import NoFile
from bson import ObjectId
from json import JSONEncoder
from .models import PatientSetting, Log, Patient, User, Room, Bed, Notification, Sensor, Video, NotificationState, ActionType
from . import onesignal_api
import paho.mqtt.client as mqtt
import secrets

def create_response(status,code,data):
    return JsonResponse({"status":status,"code":code,"data":data},safe=False)

def download_video(request, file_id):
    try:
        file_id = ObjectId(file_id)
    except:
        return HttpResponse("Invalid file ID.", status=400)

    try:
        client = MongoClient('mongodb+srv://watchdog:watchdog123456@watchdog.olmhayr.mongodb.net/')
        db = client['watchdog']
        fs = GridFS(db)
    except Exception as e:
        return HttpResponse(f"Error connecting to database: {e}", status=500)

    try:
        file = fs.get(file_id)
        response = FileResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
        return response
    except NoFile:
        return HttpResponse("File not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error retrieving the file: {e}", status=500)
        
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')

        if not video_file:
            return JsonResponse({"message": "No video file provided!"})

        video = Video(title=title)
        video.video_file.put(video_file, content_type='video/mp4')
        video.save()
        return JsonResponse({"message": "Video uploaded!", "video_id": str(video.id)}, encoder=JSONEncoderCustom)
    return JsonResponse({"message": "Unsupported HTTP method."})

class JSONEncoderCustom(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

def create_log(request):
    log = Log(actionType=ActionType.LEAVEBED, actionDescription="someone leaving bed", targetId=ObjectId())
    log.save()
    return JsonResponse({"message": "Log created!", "log_id": log.actionId}, encoder=JSONEncoderCustom)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    
        user = User(userId=user_id)
        user.save()
        return JsonResponse({"message": "User created!", "user_id": user.userId}, encoder=JSONEncoderCustom)

def create_patient_setting(request):
    patientSetting = PatientSetting(settingName="leaving_bed", scope=1)
    patientSetting.save()
    return JsonResponse({"message": "PatientSetting created!", "PatientSetting_name": patientSetting.settingName}, encoder=JSONEncoderCustom)

@csrf_exempt
def create_patient(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        bed_id = int(request.POST.get('bed_id'))

        new_patient = Patient(
            patientId=ObjectId(),
            gender=gender,
            lastName=last_name,
            firstName=first_name,
            bedId=bed_id,
            setting=[]  
        )
        new_patient.save()
        return JsonResponse({"status": "success", "message": "New patient created"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def get_patient_list(request):
    if request.method == 'GET':
        all_patients = Patient.objects.all()

        # Building Patient List Data
        patient_list_data = []
        for patient in all_patients:
            patient_data = {
                "patientId": str(patient.patientId),
                "gender": patient.gender,
                "last_name": patient.lastName,
                "first_name": patient.firstName,
                "bed_id": patient.bedId,
            }
            patient_list_data.append(patient_data)

        return JsonResponse({"status": "success", "patients": patient_list_data})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def get_patient_by_id(request, patient_id):
    if request.method == 'GET':
        patient = get_object_or_404(Patient.objects, patientId=patient_id)

        patient_data = {
            "patientId": str(patient.patientId),
            "gender": patient.gender,
            "last_name": patient.lastName,
            "first_name": patient.firstName,
            "bed_id": patient.bedId,
        }
        return JsonResponse({"status": "success", "patient": patient_data})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def publish_mqtt_message(request):
    if request.method == 'POST':
        isOpen = request.POST.get('isOpen')

        MQTT_BROKER_HOST = 'localhost'
        MQTT_BROKER_PORT = 1883
        MQTT_TOPIC = 'camera_switch'

        client = mqtt.Client()
        
        try:
            client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
            client.publish(MQTT_TOPIC, isOpen)
            response_data = {"success": True, "message": "Message has been published"}
        except Exception as e:
            response_data = {"success": False, "error": str(e)}
        return JsonResponse(response_data)

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        room_location = request.POST.get('roomLocation')
        room_number = request.POST.get('roomNumber')
        
        room = Room(roomLocation=room_location, roomNumber=room_number)
        room.save()
        
        return JsonResponse({"status": "success", "roomId": str(room.roomId)})

@csrf_exempt
def update_room(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(roomId=room_id)
        
        room_location = request.POST.get('roomLocation')
        room_number = request.POST.get('roomNumber')
        
        if room_location:
            room.roomLocation = room_location
        if room_number:
            room.roomNumber = room_number
        
        room.save()
        return JsonResponse({"status": "success", "message": "Room updated"})

@csrf_exempt
def delete_room(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(roomId=room_id)
        room.delete()
        return JsonResponse({"status": "success", "message": "Room deleted"})

@csrf_exempt
def list_rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        room_data = [{"roomId": str(room.roomId), "roomLocation": room.roomLocation, "roomNumber": room.roomNumber} for room in rooms]
        return JsonResponse({"status": "success", "rooms": room_data})

@csrf_exempt
def create_bed(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomId')
        bed_number = request.POST.get('bedNumber')
        
        bed = Bed(roomId=room_id, bedNumber=bed_number)
        bed.save()
        
        return JsonResponse({"status": "success", "bedId": str(bed.bedId)})

@csrf_exempt
def update_bed(request, bed_id):
    if request.method == 'POST':
        bed = Bed.objects.get(bedId=bed_id)
        
        room_id = request.POST.get('roomId')
        bed_number = request.POST.get('bedNumber')
        
        if room_id:
            bed.roomId = room_id
        if bed_number:
            bed.bedNumber = bed_number
        
        bed.save()
        return JsonResponse({"status": "success", "message": "Bed updated"})

@csrf_exempt
def delete_bed(request, bed_id):
    if request.method == 'POST':
        bed = Bed.objects.get(bedId=bed_id)
        bed.delete()
        return JsonResponse({"status": "success", "message": "Bed deleted"})

@csrf_exempt
def list_beds(request):
    if request.method == 'GET':
        beds = Bed.objects.all()
        bed_data = [{"bedId": str(bed.bedId), "roomId": str(bed.roomId), "bedNumber": bed.bedNumber} for bed in beds]
        return JsonResponse({"status": "success", "beds": bed_data})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            data = {"message":f"An error occurred: {str(e)}"}
            return create_response("error",400,data)
        
        if check_password(password, user.password):
            # User authenticated successfully
            token = secrets.token_hex(20)  # Generate a random token
            # TODO: Save this token in your database for later verification if necessary.
            user.token=token
            user.save()
            return create_response("success",200,{"message":"Login successfully","token":token})
        else:
            return create_response("error",401,{"message": "Invalid credentials"})

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return create_response("error",404,{"message": "Both username and password are required"})

        # Check if the user already exists
        try:
            user = User.objects.get(username=username)
            data = {"message": "Username already exists"}
            return create_response("error", 409, data)
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            data = {"message":"Multiple users found with the same username. This is a data inconsistency issue."}
            return create_response("error",500,data)
        except Exception as e:
            data = {"message":f"An error occurred: {str(e)}"}
            return create_response("error",500,data)
        
        # Create the new user
        user = User(username=username)
        hashed_password = make_password(password)
        user.password = hashed_password
        user.save()
        
        return create_response("success",200,{"message": "User created"})

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        token = request.POST.get('token')

        if not token:
            return  create_response("error",400,{"message": "Token is required"})

        try:
            user = User.objects.get(token=token)
            user.token = None 
            user.save()
            return create_response("success",200,{"message": "Successfully logged out"})
        except User.DoesNotExist:
            return create_response("error",404,{"message": "User not found"})

@csrf_exempt
def create_notification(request):
    if request.method == "POST":
        actionType = request.POST.get('actionType')
        sensorId = request.POST.get('sensorId')
        videoId = request.POST.get('videoId')

        head = 'Mike Leaving bed' if actionType == ActionType.LEAVEBED else 'Mike Leaving room'
        content = '' if not videoId else videoId
        state = NotificationState.UNDO

        # need to be fixed after patient and bed feature update
        # for judge no bond condition(no bed? no patient? sensor no register?)
        # try:
        #     sensor = Sensor.object.get(sensorId=sensorId)
        #     bedId = sensor.bedId
        #     if not bedId:
        #         data = {"Please bond bed"}
        #         return create_response("error",404,data)
        #     bed = Bed.object.get(bedId=bedId)
        #     patientId = bed.patientId
        #     patient = Patient.object.get(patientId=patientId)

        # except Sensor.DoesNotExist:
        #     data = {"Current device have not been registered"}
        #     return create_response("error",404,data)
        # except Exception as e:
        #     data = {"message":f"An error occurred: {str(e)}"}
        #     return create_response("error",500,data)

        try: 
            notification = Notification(sensorId=sensorId)
            notification.head = head
            notification.content = content
            notification.state = state
            notification.actionType = actionType
            notification.userId = ''

            notification.save()
            
            onesignal_api.send_notification(content,head, notification.id)
            return create_response("success",200,{"message":"Notification created"})
        except Exception as e:
            data = {"message":f"An error occurred: {str(e)}"}
            return create_response("error",500,data)

@csrf_exempt
def register_sensor(request):
    if request.method == 'POST':
        sensorId = request.POST.get('sensorId')
        sensorType = request.POST.get('sensorType')
        bedId = request.POST.get('bedId')
        
        if not sensorType or not sensorId:
            return create_response("error",404,{"message": "Both sensorId and sensorType are all required"})

        # Check if the user already exists
        try:
            sensor = Sensor.objects.get(sensorId=sensorId)
            data = {"message": "Sensor already exists"}
            return create_response("error", 409, data)
        except Sensor.DoesNotExist:
            pass
        except Exception as e:
            data = {"message":f"An error occurred: {str(e)}"}
            return create_response("error",500,data)
        
        # Create the new user
        sensor = Sensor(sensorId=sensorId)

        sensor.sensorType = sensorType
        if bedId:
            sensor.bedId = bedId

        sensor.save()
        return create_response("success",200,{"message": "Sensor created"})

@csrf_exempt
def get_notification_list(request):
    if request.method == 'GET':
        notification_list = Notification.objects.all()
        notification_data = [{"notificationId": str(notification.notificationId),"head": str(notification.head), "state": str(notification.state)} for notification in notification_list]
        return create_response("success",200,{"message": "Get all notification","data":notification_data})

@csrf_exempt
def get_notification_by_id(request, notificationId):
    if request.method == 'GET':
        try:
            notification = Notification.objects.get(notificationId=notificationId)

            user_data = None
            if notification.userId:
                try:
                    user = User.objects.get(username=notification.userId)
                    user_data = {
                        "username": user.username,
                        # 添加其他你想要的user字段，如 "email": user.email 等
                    }
                except User.DoesNotExist:
                    user_data = None

            notification_data = {
                "notificationId": str(notification.notificationId),
                "sensorId": notification.sensorId,
                "head": notification.head,
                "content": notification.content,
                "state": notification.state,
                "actionType": notification.actionType,
                "user": user_data
            }

            return create_response("success", 200, {"message": "Get notification", "data": notification_data})

        except Notification.DoesNotExist:
            return create_response("success", 404, {"message": "No such notificationId"})

@csrf_exempt
def update_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        user_token = request.POST.get('user_token')
        state = request.POST.get('state')

        try:
            # Use your method to fetch user_id from user_token
            # Suppose the method is named `get_user_id_from_token`
            user = User.objects.get(token=user_token)
            user_id = str(user.userId)

            notification = Notification.objects.get(notificationId=notification_id)

            # Check if user ids match or if the notification's userId is None
            if notification.userId and notification.userId != user_id:
                return create_response("error", 403, {"message": "Permission Denied"})

            if not notification.userId:
                notification.userId = user_id

            # Check if state matches the current state of the notification
            if state != notification.state:
                return create_response("error", 401, {"message": "State mismatch"})

            # Update state to the next stage
            if notification.state == NotificationState.UNDO.value:
                notification.state = NotificationState.IN_PROCESS.value
            elif notification.state == NotificationState.IN_PROCESS.value:
                notification.state = NotificationState.DONE.value
            # If state is already DONE, you can decide to either leave it as it is
            # or return a message indicating that the notification is already processed.

            notification.save()  # Save the updated notification state to the database

            return create_response("success", 200, {"message": "Notification updated successfully", "state": notification.state})

        except Notification.DoesNotExist:
            return create_response("error", 404, {"message": "Notification not found"})