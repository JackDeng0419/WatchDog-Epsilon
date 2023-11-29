import requests
import socket
import uuid


def send_ip():
	print("send ip")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_address = s.getsockname()[0]
	s.close()
	print(ip_address)
	mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
	url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/register/'

	data = {
		'sensorId': mac_address,
		'sensorType': "CAMERA",
		'sensorIp': ip_address
	}

	response = requests.post(url, data=data)
	print(response.text)
	return ip_address
    


if __name__ == '__main__':
    send_ip()
