


import sys
import os
import time
import subprocess
import requests
import random
import base64
import string
import time
import json
import http.client
import re




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

def get_https_response(url):
    if not url.startswith("https://"):
        raise ValueError("Sorun Oluştu")
    host = url.split("/")[2]
    path = "/" + "/".join(url.split("/")[3:])
    connection = http.client.HTTPSConnection(host)
    connection.request("GET", path, headers=headers)
    response = connection.getresponse()
    cookies = response.getheader("Set-Cookie")
    body = response.read().decode('utf-8')
    if cookies:
        match = re.search(r"token=([a-fA-F0-9]+)", cookies)
        if match:
            return match.group(1)
    return None


def rndm(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


domain = "zylofy.dev.tc"
#print(domain)
fake_ip = random_ip()
rndom = rndm()
host = "api.2nr.xyz"
endpoint = "/auth/register"

headers = {
    "Host": host,
    "Content-Type": "application/json; charset=UTF-8",
    #"Accept-Encoding": "gzip",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "X-Forwarded-For": fake_ip
}

data = {
    "query": {
        "email": f"{rndom}@{domain}",
        "imei": "950c2c1f4b27e27ryuga",
        "password": "Zsezsert3169#"
    },
    "id": 103
}

json_data = json.dumps(data)
connection = http.client.HTTPSConnection(host)
connection.request("POST", endpoint, body=json_data, headers=headers)
response = connection.getresponse()
response_data = response.read().decode("utf-8")
print(response_data)
response_json = json.loads(response_data)

if response_json.get("success", None) == True:
    print(f"[+] Hesap Oluşturuluyor")
else:
    print("Hesap Oluşturulurken Hata")
    print(response_json)
    raise SystemExit()

email = f"{rndom}@{domain}"
count = 1
token = None
print(email)
while True:
    time.sleep(5)
    try:
        mail = requests.get(f"https://mailsorgu.com/api/messages/{email}/gFqNIYXC7oM8H961fcux").json()[0]["content"]
        pattern = r"https://api\.2nr\.xyz/register/\?email=[^&]+&amp;token=[a-f0-9]{64}"
        sonuc = re.search(pattern, mail)
        if sonuc:
            urlx = sonuc.group().replace("&amp;", "&")
            token = get_https_response(urlx)
            break
    except Exception as e:
        print(f"\r[{count}] Hesap Doğrulanıyor.\r",end="")
        count += 1
        continue

conn = http.client.HTTPSConnection("api.2nr.xyz")
payload = "{\"id\":300}"

headers.update({
    'Cookie': f"token={token}; x-app-version=49"
})

conn.request("POST", "/numbers/getRandomNumber", payload, headers)
res = conn.getresponse()
data = res.read().decode("utf-8")
response_json = json.loads(data)

if response_json and isinstance(response_json, list):
    num_id = response_json[0].get("id")
    number = response_json[0].get("number")
else:
    print( f"Bir Hata Oluştu{reset}", response_json)
    raise SystemExit()


payload2 = "{\"query\":{\"availability_days\":[1,2,3,4,5,6,7],\"color\":\"#E63147\",\"hour_from\":null,\"hour_to\":null,\"integrity_token\":\"eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2R0NNIn0.RD4CJzgbGoUWs_27NfVaDyrAV-hEx5UYloXJLxK1CTHSP9zLXWEahg.JrYhtgRPj7mXjMcZ.k2Yd7ETCsSAvMxmMMYNl04Iz6WNpiGtAobgDtDT5WuhOX95vpFkBfXzCMDBxBS3obITFjsF09p4heFNaNZawQNJRt0WBcTFfuhJ9a01YYaaJFvQI-Lx8-xPIhQdENLE1dUchYfKBJP7e9-Jy0mr4-gXrlF570OnZuw_pgPkrWdEAifVuj49pOt64x7dS46LIfjG81aILT-hP8YkS97qyQfZ8MLec10ylIztjsKebU5XEavnfK_2VFnTB0Gc2QtPlyOjFuEIkBUl6ck1bRwRoeZtAtaL7w7nnVXPP0ZTcg3tTRN55OypLYTL7LvKHZ-hS16Bf4xmQWEBFeqWn0CEfu7Z4cub0yrkCq8j8uwPDQfPvimLIU-bvWF6BkE5eIMtPgqEXPDWuNwMEQAxIrvCaunCannHNtEjstt7ePIA9UYQ7umq6CL6aAZRCAYKVBPUAMOzaoT0iWKtvKhHhQ6o0CJPzjsi1M21BvAhpDz35EuwCm1xVXf2mSDmv1DDOr4yNGlik91zsLl1ZWq8a-vH9w0g3YWI5uftXTmTfnjWIB3iuZ77TM9dwmFVQObAGlKg5TMQ8X-AcZMLdtt8DPLPT-egpyNUgkEuAX6_txp_hsZff5HU59Q7wOETrzawgXJuFmqpGNYYD6-1Uo26wx2AqkkjfmtFk0SYzD4rnTbAXEOX2PPVLYH2cR5IEGoQEBGOdQvZCpGhn9krZv_MllLqnjP03NxGFAfuwMzamPNlt6Bd7Vq2yvH9_BGHv.Qn4Y2lP_16iVrMuxNT420g\",\"marketing\":true,\"name\":\"whoisryuga\",\"nonce\":\"azlwbm02ZnIwYXVwZDM2YjhrNWNrOGEwYnE\",\"number_id\":"+str(num_id)+"},\"id\":301}"

conn.request("POST", "/numbers/reserveNumber", payload2, headers)
res = conn.getresponse()
data = res.read().decode("utf-8")
tt = json.loads(data).get("success")
if tt == True:
	pass
else:
	print(p_kirmizi+"Numara Alınırken Hata"+reset)
	raise SystemExit()
	
payload3 = "{\"id\":400}"


while True:
	logo()
	print(f"║ Hesap Oluşturuldu\n╚>> +48 {number}\n")
	print(f"••• 2Nr Manuel Kullanmak İstiyorsan\n[@] Email ᯓ★ {email}\n[#] Şifre ᯓ★ Zsezsert3169#\n")
	conn.request("POST", "/sms/get", payload3, headers)
	res = conn.getresponse()
	data2 = res.read().decode("utf-8")
	gg = json.loads(data2)
	try:
		for item in gg['result']:
			print(item)
		qq = input(f"[+] Yenilemek İçin Enter'e Çıkmak İçin C'ye Yaz: ").lower()
		if qq == "c":
			break
		continue
	except:
		print(f"[×] Gelen Kutusu Boş",gg)
		qq = input(f"[+] Yenilemek İçin Enter'e Çıkmak İçin C'ye Yaz: ").lower()
		if qq == "c":
			break
		continue
