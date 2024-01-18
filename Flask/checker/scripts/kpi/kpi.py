from datetime import datetime
import time
import json
import os
import requests
import time
import requests
import sys
import socketio

http_session = requests.Session()
http_session.verify = False
sio = socketio.Client(logger=False, engineio_logger=False)

broker_name="orion-1"
username = ""
password = ""
variable="value44"
kpi_id=""
access_token=""
try:
    username=sys.argv[1]
    password=sys.argv[2]
except Exception as E:
    print("Operation failed due to",E)
    exit(1)

root_path = os.getcwd()
params_path = root_path + "/data/conf.json"
f = open(params_path)
conf= json.load(f)

####
def getTokenViaUserCredentials():
    payload = {
        'f': 'json',
        'client_id': 'js-kpi-client',
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    urlToken = f"{conf['url']}/auth/realms/master/protocol/openid-connect/token"
    response = requests.request("POST", urlToken, data=payload, headers=header)
    token = response.json()
    return token

@sio.event
def connect():
    token = getTokenViaUserCredentials()
    sio.emit("authenticate",token['access_token'])

@sio.event
def authenticate(data):
    jd = json.loads(data)
    if jd['status']=='OK':
        sio.emit('subscribe',str(kpi_id))
    else:
        print("Synoptics: [ERROR] in authenticate: ",str(jd))
        exit(-1)

@sio.event
def subscribe(data):
    print("data received in subscribing", data)
    r = json.loads(data)
    if r['status'] == 'OK':
        sio.on("update "+str(kpi_id), handle_update)
    else:
        print("Synoptics: [ERROR] in subscribe: ",str(r))
        exit(-1)
        
        
def handle_update(data):
    print("Data updated with",data)
    globals()['latest_data']=json.loads(data)['lastValue']
    sio.disconnect()

@sio.event
def disconnect():
    print('Disconnected from server')
####


def main():
    
    print("Configuration file opened")
    access_token = accessToken(conf)
    globals()['kpi_id']=createKpi(conf,access_token)
    for i in range(5):
        sendDataKpi(kpi_id,conf,access_token,str(i))
        getKpi(kpi_id,conf,access_token,str(i))
        sio.connect(url=conf['url'],socketio_path='synoptics/socket.io',transports='websocket')
        sio.wait()
        sio.disconnect()
        if globals()['latest_data'] == i:
            print("Data sent matched data received from synoptics")
        else:
            print("[Error] Data did not match data received from synoptics")
        
            
def getKpi(idKpi,conf, token, base_to_check):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["url"] + '/datamanager/api/v1/kpidata/'+str(idKpi)+'/values/?sourceRequest=iotapp&highLevelType=MyKPI"&last=1'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request was successful: the kpi was received")
        if response.json()[0]["value"]==str(base_to_check)+'.0':
            print("Data sent matched data received from KPI")
        else:
            print("[Error] Data sent did not match data received from KPI")
            print("Response:")
            print(response.json())
    else:
        print(f"[Error] Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)

def sendDataKpi(idKpi,conf, token, value):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["url"] + '/datamanager/api/v1/kpidata/'+str(idKpi)+'/values/?sourceRequest=iotapp'

    data = {
        "kpiId": idKpi,
        "value": value,
        "dataTime": int(time.time() * 1000)
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful: some data was sent to the kpi")
    else:
        print(f"[Error] Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)


def createKpi(conf, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["url"] + '/datamanager/api/v1/kpidata/?sourceRequest=kpieditor'

    data = {
        "highLevelType": "MyKPI",
        "valueName": "countingWifiLast",
        "description": "tryKPI",
        "info": "newKPI",
        "metadata": [
            {"key": "note"},
            {"key": "address"},
            {"key": "civic"},
            {"key": "city"},
            {"key": "province"},
            {"key": "phone"},
            {"key": "fax"},
            {"key": "website"},
            {"key": "email"}
        ],
        "nature": "TourismService",
        "subNature": "Wifi",
        "valueUnit": "#",
        "valueType": "people_count",
        "dataType": "integer",
        "latitude": "43.785905",
        "longitude": "11.228027"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful: a new kpi was created")
        print("Response:")
        print(response.json())
    else:
        print(f"[Error] Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)
    print("id of kpi:", response.json()['id'])
    return response.json()['id']



def accessToken(conf):
    access_token = ''
    payload = {
        'f': 'json',
        'client_id': conf.get('token').get('clientID'),
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    urlToken = conf.get('token').get('token_url')
    currentTime = datetime.now()
    try:
        response = requests.request("POST", urlToken, data=payload, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(currentTime, "[Error] Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print(currentTime, "[Error] Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print(currentTime, "[Error] Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print(currentTime, "[Error] Ops: Something Else", err)
    else:
        token = response.json()
        print("The access token was correctly collected")
        access_token = token['access_token']

    return access_token


if __name__ == "__main__":
    main()
