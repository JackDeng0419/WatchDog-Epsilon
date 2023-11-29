from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import time

class Command(BaseCommand):
    help = 'Run the MQTT subscriber'

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("temperature")

    def on_message(self, client, userdata, msg):
        print("Received message: " + msg.topic + " -> " + msg.payload.decode('utf-8'))

    def handle(self, *args, **kwargs):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("localhost", 1883, 60)
        client.loop_start()

        try:
            while True:
                time.sleep(1)  # Keep the program running.
        except KeyboardInterrupt:
            print("Exiting...")
            client.loop_stop()
