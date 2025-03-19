
import sys
import os
import time
import subprocess
import random
import base64
import string
import json
import http.client
import re
from curl_cffi import requests

s = requests.Session()

def get_https_response(url,headers):
    if not url.startswith("https://"):
        raise ValueError("Sorun Oluştu")
    host = url.split("/")[2]
    path = "/" + "/".join(url.split("/")[3:])
    response = requests.get(f"https://{host}{path}", headers=headers)
    cookies = response.headers.get("Set-Cookie", "")
    print(cookies)
    body = response.text
    match = re.search(r"token=([a-fA-F0-9]+)", cookies)
    if match:
        return match.group(1)

    return None


def logo():
    print(f"""
    ________              ______              
    ___  __ \_____ __________  /__ 
    __  / / /  __ `/_  ___/_  //_/ 
    _  /_/ // /_/ /_  /   _  ,<   
    /_____/ \__,_/ /_/    /_/|_|ENZA""")
    print("  2NR Fake No Tool V1.2")
    print("")
    
logo()

def rndm(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

domain = "zylofy.dev.tc"
fake_ip = random_ip()
rndom = rndm()
host = "api.2nr.xyz"
endpoint = "/auth/register"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.10.0",
    "X-Forwarded-For": fake_ip
}

data = {
    "query": {
        "email": f"{rndom}@{domain}",
        "imei": "d1eae8b74a2fe12e",
        "password": "Zsezsert3169#"
    },
    "id": 103
}

response = s.post(f"https://{host}{endpoint}", json=data, headers=headers)
response_json = response.json()

if response_json.get("success", None) == True:
    print(f"[+] Hesap Oluşturuluyor")
else:
    print("Hesap Oluşturulurken Hata")
    print(response_json)
    raise SystemExit()
