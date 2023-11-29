# test
# test pi

import requests
import os
import bluetooth_handle
import subprocess
import uuid
import thermal.pixels_test as thermal_detect
import socket

def start_workflow():
    
    
    while is_wifi_connected() is not True:
        subprocess.run(['sudo', 'python3', 'bluetooth_handle.py'])
        
    
        
    print("start detection")
    
    mqtt_topic = init_register()
    thermal_detect.run(mqtt_topic=mqtt_topic)
    #subprocess.run(['python3', 'mediaPipe_obj_detection/raspberry_pi/detect.py', mqtt_topic])
    
    
    
def is_wifi_connected():
    response=os.system("ping -c 1 google.com")
    return True if response == 0 else False
    
def init_register():
    print("register device")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    print(ip_address)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/register/' # replace with your server's API endpoint

    data = {
        'sensorId': mac_address,
        'sensorType': "THERMAL",
        'sensorIp': ip_address
    }

    response = requests.post(url, data=data)
    print(response.text)
    mqtt_topic = mac_address
    return mqtt_topic
    


if __name__ == '__main__':
    start_workflow()
