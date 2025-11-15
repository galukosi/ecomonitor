# This script allows you to send HTTP requests that real Guard-Devices do

import requests
import json
import time
import random

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

url = input("Enter endpoint API URL (default: http://0.0.0.0:8000/api/sensor-readings/):")
if url == "":
    url = "http://0.0.0.0:8000/api/sensor-readings/"

device_id = input("Enter device id (default: GG-A5080814): ")
if device_id == "":
    device_id = 'GG-A5080814'


while True:
    data = {
        "device_id": device_id,
        "final_value": 24,
        "raw_value": random.randint(200, 300),
        "voltage": round(random.uniform(0.1, 0.3), 6)
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print("Status code:", response.status_code)
    print("Response:", response.text)
    time.sleep(3)
