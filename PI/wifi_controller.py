import subprocess
import requests
import time
import os
import socket

def set_wifi(ssid, psk):
	get_wifi_config_permisson()
	wifi_config_template = """
network={{
	ssid="{ssid}"
	psk="{psk}"
	key_mgmt=WPA-PSK
}}
"""
	
	wifi_config = wifi_config_template.format(ssid=ssid, psk=psk)
	
	file_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
	
	with open(file_path, 'a') as file:
		file.write(wifi_config)
		
	print(f"Added Wi-Fi network: {ssid} to {file_path}")
	restart_wifi_interface()
	print("wifi restarted, wifi connecting...")
	ssid = check_wifi_connection()
	if ssid:
		print("connected to WiFi:", ssid)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
		s.connect(("8.8.8.8", 80))
		ip_address = s.getsockname()[0]
		s.close()
		print(ip_address)
		return ip_address
	else:
		print("Not connected to any WiFi after 20s.")
		return None
	

def get_wifi_ssid():
	try:
		result = subprocess.check_output(['iwconfig', 'wlan0']).decode('utf-8')
		for line in result.split('\n'):
			if 'ESSID' in line:
				# extract the SSID from the line
				ssid = line.split(':')[1].strip().replace('"', '')
				return ssid
		return None
	except Exception as e:
		print(e)
		return None
	
def check_wifi_connection():
	for _ in range(60):
		print("wifi connecting...")
		ssid = get_wifi_ssid()
		print(ssid)
		if ssid and ssid!="off/any":
			response=os.system("ping -c 1 -W 10 google.com")
			print(f"!!!!!!ping google: {response}")
			if response == 0:
				return ssid 
		time.sleep(1)
	return None
	
	
def restart_wifi_interface():
	
	subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)
	
def get_wifi_config_permisson():
	subprocess.run(['sudo', 'chmod', '777', '/etc/wpa_supplicant/wpa_supplicant.conf'], check=True)
	
	
if __name__ == '__main__':
	set_wifi("13mini", "dzj000419")
