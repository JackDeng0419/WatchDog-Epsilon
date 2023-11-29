import subprocess
from bluetooth import *
import wifi_controller

def start():
	def connect_to_wifi(ssid, password):
		ip = wifi_controller.set_wifi(ssid, password)
		return ip
			
		# # Use wpa_supplicant to set wifi credentials
		# cmd = [
			# 'wpa_passphrase', ssid, password
		# ]
		# psk = None
		# try:
			# result = subprocess.run(cmd, capture_output=True, text=True)
			# for line in result.stdout.split('\n'):
				# if 'psk=' in line:
					# psk = line.split('=')[1]
		# except Exception as e:
			# print("Error getting PSK:", e)
			# return

		# # Assuming you are using wlan0 as your wifi device
		# cmd = f'wpa_cli -i wlan0 set_network 0 ssid \'" {ssid} "\' && wpa_cli -i wlan0 set_network 0 psk {psk} && wpa_cli -i wlan0 enable_network 0 && wpa_cli -i wlan0 reassociate'.split()
		# try:
			# subprocess.run(cmd)
			# print("WiFi should be connecting now!")
		# except Exception as e:
			# print("Error setting wifi:", e)
		

	server_sock = BluetoothSocket(RFCOMM)
	server_sock.bind(("", PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	advertise_service(server_sock, "SampleServer",
					  service_id=uuid,
					  service_classes=[uuid, SERIAL_PORT_CLASS],
					  profiles=[SERIAL_PORT_PROFILE],
					  )

	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)
	

	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0:
				break

			# Convert data to string
			data = str(data, encoding="utf-8")
			print("received [%s]" % data)

			# Check if data contains the separator ";"
			if ";" in data:
				wifi_name, wifi_password = data.split(";")
				wifi_password = wifi_password.strip()
				ip = connect_to_wifi(wifi_name, wifi_password)
				client_sock.send(ip)
				client_sock.send("  ")

			client_sock.send(data)
			client_sock.close()
			server_sock.close()
			print("all done successfully")
	except:
		client_sock.close()
		server_sock.close()
		print("errors in wifi connection")
		
if __name__ == '__main__':
	start()
