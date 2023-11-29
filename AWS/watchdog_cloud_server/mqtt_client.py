import paho.mqtt.client as mqtt
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "watchdog_cloud_server.settings")

import django
django.setup()

from watchdog_cloud_server.views import create_log 

MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST', 'localhost')
MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', 1883))
MQTT_KEEP_ALIVE_INTERVAL = 60

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("temperature")  

def on_message(client, userdata, msg):
    request = None
    create_log(request)
    print(f"Temperature topic: {msg.topic}, Payload: {msg.payload.decode('utf-8')}")  

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_KEEP_ALIVE_INTERVAL)
client.loop_start()

try:
    while True:
        time.sleep(1)  # Keep the program running.
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
