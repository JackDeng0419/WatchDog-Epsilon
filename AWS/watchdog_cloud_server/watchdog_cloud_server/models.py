from django.db import models
from mongoengine import FileField,Document, DateTimeField,StringField, ObjectIdField, EmbeddedDocument, IntField,EmbeddedDocumentListField, SequenceField
from django.conf import settings
from mongoengine import connect
from enum import Enum
import datetime
import mongoengine

connect(db=settings.MONGODB['db'], host=settings.MONGODB['host'])

class Video(Document):
    title = StringField()
    video_file = FileField()
    
class Role(Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class ActionType(Enum):
    LEAVEBED = "LEAVEBED"
    LEAVEROOM = "LEAVEROOM"

class NotificationState(Enum):
    UNDO = "UNDO"
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"

class SensorType(Enum):
    THERMAL = "THERMAL"
    CAMERA = "CAMERA"

class PatientSettingItem(EmbeddedDocument):
    patientSettingId = SequenceField(primary_key=True)
    value = StringField(max_length=50)

class Patient(Document):
    patientId= ObjectIdField(primary_key=True) 
    gender= StringField(choices=[gender.value for gender in Gender])
    lastName= StringField(max_length=25)
    firstName= StringField(max_length=25)
    bedId= IntField()
    setting = EmbeddedDocumentListField(PatientSettingItem)

class User(Document):
    userId = mongoengine.fields.SequenceField(primary_key=True)
    username = StringField(max_length=100)
    password= StringField(max_length=100)
    lastName= StringField(max_length=25)
    firstName= StringField(max_length=25)
    role = StringField(choices=[role.value for role in Role])
    token= StringField(max_length=50)
    tokenExpiresTime= models.DateTimeField(auto_now_add=True)

class PatientSetting(Document):
    patientSettingId= SequenceField(primary_key=True)
    settingName= StringField(max_length=25)
    scope= IntField()

class Room(Document):
    roomId= ObjectIdField(primary_key=True)
    roomLocation = StringField(max_length=50)
    roomNumber = IntField()

class Bed(Document):
    bedId= SequenceField(primary_key=True)
    roomId= ObjectIdField()
    bedNumber= IntField()
    patientId= StringField(max_length=50)

class Log(Document):
    actionId = SequenceField(primary_key=True)
    actionType = StringField(choices=[type.value for type in ActionType])
    actionDescription = StringField(max_length=255)
    actionTime = DateTimeField(default=datetime.datetime.utcnow)
    targetId = ObjectIdField()


class Notification(Document):
    notificationId = mongoengine.fields.SequenceField(primary_key=True)
    userId = StringField(max_length=100)
    sensorId = StringField(max_length=100)
    head = StringField(max_length=25)
    content = SequenceField(max_length=255)
    state = StringField(choices=[type.value for type in NotificationState])
    actionType = StringField(choices=[type.value for type in ActionType])


class Sensor(Document):
    sensorId = StringField(max_length=100)
    sensorType = StringField(choices=[type.value for type in SensorType])
    bedId = StringField(max_length=100)

