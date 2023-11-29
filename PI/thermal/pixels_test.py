#!/usr/bin/python
# Copyright (c) 2017 Adafruit Industries
# Author: Dean Miller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep
import requests
import paho.mqtt.client as mqtt
import threading

#import Adafruit_AMG88xx.Adafruit_AMG88xx as AMG88

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = Adafruit_AMG88xx()

# Optionally you can override the bus number:
#sensor = AMG88.Adafruit_AMG88xx(busnum=2)

#wait for it to boot

isStop = False
mqtt_topic_global = None
avg_temp = 0


def send_alive_check():
    global mqtt_topic_global
    while True:
        print("alive checking"+mqtt_topic_global)
        url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/report_alive/'
        data = {'sensorId': mqtt_topic_global}
        response = requests.post(url, data=data)
        print(response.text)
        sleep(10)  # Wait for 10 seconds before sending the next request.

def update_avg_temp():
	global avg_temp
	# Spend 10 seconds to get the average temperature from the thermal sensor
	temp_readings = []
	for _ in range(10):  # 10 readings over 5 seconds (2-second interval)
		temperature = sensor.readPixels()
		sub_max_temp = max(temperature)
		temp_readings.append(sub_max_temp)
		print(sub_max_temp)
		sleep(0.5)
	avg_temp = sum(temp_readings) / len(temp_readings)
	print(f"Updated average temperature: {avg_temp}")
	print("sending newest avg temp")
	url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
	data = {'lastTemp': avg_temp}
	response = requests.post(url, data=data)
	print(response.text)

def run(mqtt_topic):
	previous_avg_tem = 0
	request_send = False
	first_read = True
	global mqtt_topic_global
	mqtt_topic_global = mqtt_topic
	
	print("sending newest detection state")
	url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
	data = {'is_enable': 'true'}
	response = requests.post(url, data=data)
	print(response.text)
	
	# mqtt
	BROKER_ADDRESS = "1.tcp.au.ngrok.io"
	MQTT_TOPIC = mqtt_topic


	def on_connect(client, userdata, flags, rc):
		print(f"Connected with result code {rc}")
		client.subscribe(MQTT_TOPIC)

	def on_message(client, userdata, msg):
		print(f"{msg.topic} {str(msg.payload)}")
		message = msg.payload.decode("utf-8")
		print(message)
		global isStop
		if message == "STOP":
			print("detection stopped")
			isStop = True
			print("sending newest detection state")
			url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
			data = {'is_enable': 'false'}
			response = requests.post(url, data=data)
			print(response.text)
		elif message == "START":
			print("detection start")
			isStop = False
			print("sending newest detection state")
			url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
			data = {'is_enable': 'true'}
			response = requests.post(url, data=data)
			print(response.text)
		elif message == "UPDATETEMP":
			print("update temperature")
			update_avg_temp()
	  

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(BROKER_ADDRESS, 26540, 60)

	client.loop_start()
	
	
	# Start a new thread to send the alive check request every 30 seconds
	alive_check_thread = threading.Thread(target=send_alive_check)
	alive_check_thread.daemon = True  # This makes sure the thread will exit when the main program exits
	alive_check_thread.start()
	
	previous_avg_tem = 0
	maxtemp = 0
	request_send = False
	first_read = True
	
	update_avg_temp()

	while(1):
		global avg_temp
		if isStop is True:
			continue
		else:
			if first_read:
				first_read = False
				continue
			temperature = sensor.readPixels()
			current_avg_tem = sum(temperature) / len(temperature)
			sub_max_tem = max(temperature)
			air_upper_bound = avg_temp + 3
			human_lower_bound = air_upper_bound + 3
			print(sub_max_tem, maxtemp)
			if sub_max_tem > maxtemp:
				maxtemp = sub_max_tem
			if maxtemp - sub_max_tem > 3 and sub_max_tem < air_upper_bound and maxtemp > human_lower_bound: # 25：prevent hand close （point 3）； 28： prevent walk by
				maxtemp = sub_max_tem
				res =requests.get('http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/log/create/')
				print(res)
				print('sent quest!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				notification_response = requests.post('http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/notification/create/', data={'actionType': 'LEAVEBED', 'sensorId': '2', 'videoId':'123'})
				print(notification_response.text)
	
