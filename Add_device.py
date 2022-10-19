#!/usr/bin/env test
awda

import time
import requests
from auth_token import get_token

def main():
	
	token = get_token()
	
	
	api_path = "https://sandboxdnac2.cisco.com/dna"
	headers = {"Content-Type": "application/json", "X-Auth-Token": token}

	new_device_dict = {
	"ipAddress": ["1.2.3.4"],
	"snmpVersion": "v2",
	"snmpROCommunity": "readonly",
	"snmpRWCommunity": "readwrite",
	"snmpRetry": "1",
	"snmpTimeout": "60",
	"cliTransport": "ssh",
	"userName": "test",
	"password": "test",
	"enablePassword": "secrets",
	}
	
	add_resp = requests.post(
		f"{api_path}/intent/api/v1/network-device",
		 headers=headers, 
		 json=new_device_dict,
		 )
	print("add_resp")
	if add_resp.ok:
		
		print(f"Request accepted: status code {add_resp.status_code}")
		time.sleep(10)
		
		task = add_resp.json()["response"]["taskId"]
		task_resp = requests.get(f"{api_path}/intent/api/v1/task/{task}", headers=headers)
		
		if task_resp.ok:
			task_data = task_resp.json()["response"]
			if not task_data["isError"]:
				print("New deice succesfully added")
			else:
				print(f"Async task error seen: {task_data['progress']}")
		else:
			print(f"Async GET failed: status code {task_resp.status_code}")
	
	else:
		print(f"Device addition failed with code {add_resp.status_code}")
		print(f"Failure body: {add_resp.text}")
