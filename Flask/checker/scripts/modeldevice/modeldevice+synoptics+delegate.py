from datetime import datetime
import time
import json
import os
import sys
import socketio
import requests

http_session = requests.Session()
http_session.verify = False
sio = socketio.Client(logger=False, engineio_logger=False)
import requests

f = open("data/conf.json")
config = json.load(f)

latest_data = None
broker_name="orion-001"
username = ""
password = ""
synoptics = ""
try:
    username=sys.argv[1]
    password=sys.argv[2]
    synoptics=sys.argv[3]
except Exception as E:
    print("Operation failed due to",E)
    print("Are you sure you gave the correct number of parameters? (username, password, test the synoptics)")
    exit(1)

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

    urlToken = f"{config['base-url']}/auth/realms/master/protocol/openid-connect/token"
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
        sio.emit('subscribe','http://www.disit.org/km4city/resource/iot/orion-1/Organization/'+get_latest_device()+' value44')
    else:
        print("Synoptics: [ERROR] in authenticate: ",str(jd))

@sio.event
def subscribe(data):
    print("data received in subscribing", data)
    r = json.loads(data)
    if r['status'] == 'OK':
        sio.on('update http://www.disit.org/km4city/resource/iot/orion-1/Organization/'+get_latest_device()+' value44', handle_update)
    else:
        print("Synoptics: [ERROR] in subscribe: ",str(r))
        
        
def handle_update(data):
    print("Data updated with",data)
    globals()['latest_data']=json.loads(data)['lastValue']
    sio.disconnect()

@sio.event
def disconnect():
    print('Disconnected from server')

def main():
    
    access_token = accessToken(config)
    model_name = datetime.now().strftime("%Y%m%dT%H%M%S")
    device_name = datetime.now().strftime("%Y%m%dT%H%M%S")
    
    with open('latest-model.txt', 'w') as f:
        f.write(model_name+'model')
    with open('latest-device.txt', 'w') as f:
        f.write(device_name+'device')
    createModel(config, access_token)
    
    createDevice(config, access_token, get_latest_device())

    uriDelegateDevice = delegateDevice(device_name+'device', config, access_token)
    if synoptics == "True":
        nData = 3
        sleep = 5
        previous_data = latest_data
        for i in range(0, nData):
            print('\n')
            string_value = str(i)
            sendData(config, accessToken(config), get_latest_device(), string_value)
            
            print("Waiting", str(sleep), "seconds")
            time.sleep(sleep)
            access_token_delegated = accessTokenDelegated(config)
            readDelegateDevice(uriDelegateDevice, config, access_token_delegated, string_value)
            
            print("Waiting another", str(sleep), "seconds")
            time.sleep(sleep)
            sio.connect(url=config['base-url'],socketio_path='synoptics/socket.io',transports='websocket')
            sio.wait()
            sio.disconnect()
            if str(latest_data)==string_value:
                print("Data was received from synoptics")
            else:
                print(latest_data, string_value)
                print("Error: data was not received")
            if (previous_data==None):
                pass # first time setting a value
            elif (previous_data!=latest_data):
                print("Success: update was read as intended")
            else:
                print("Failure: the newest value wasn't read")
    deletedevice(get_latest_device(), broker_name, access_token,config["model"]["model_url"])

def readDelegateDevice(serviceuri, conf, token, value_read):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["base-url"] + '/superservicemap/api/v1/?serviceUri='+ serviceuri +'&realtime=true&appID=iotapp'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        if value_read==response.json()["realtime"]["results"]["bindings"][0]["value44"]["value"]:
            print("Servicemap: read expected value")
        else:
            print("Servicemap: [ERROR] didn't read correct value; got", response.json()["realtime"]["results"]["bindings"][0]["value44"]["value"], ", expected", value_read)
        #print("Request was successful.")
        #print("Response:")
        #print(response.json())
    else:
        print(f"Servicemap: [ERROR] request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)

def createModel(conf, token):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    url = conf["model"]["model_url"] + f"action=insert&attributes=%5B%7B%22value_name%22%3A%22dateObserved%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22timestamp%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22timestamp%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%2C%7B%22value_name%22%3A%22value44%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22message%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22-%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%5D&name={get_latest_model()}&description=&type={conf['model']['model_type']}&kind={conf['model']['model_kind']}&producer=&frequency={conf['model']['model_frequency']}&kgenerator={conf['model']['model_kgenerator']}&edgegateway_type=&contextbroker={conf['model']['model_contextbroker']}&protocol={conf['model']['model_protocol']}&format={conf['model']['model_format']}&hc={conf['model']['model_hc']}&hv={conf['model']['model_hv']}&subnature={conf['model']['model_subnature']}&static_attributes=%5B%5D&service=&servicePath=&token={token}&nodered=true"
    response = requests.request("PATCH", url, headers=header)
    r = (response.text)
    r = json.loads(r)
    print(f"\nStatus for model {get_latest_model()}: " + r['status'])
    time.sleep(2)

def createDevice(conf, token, device_name):
    long = "11.24657"
    lat = "43.77709"

    header = {
        "Content-Type": "application/json",
        "Accept": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}",
    }
    
    url = conf["device"]["device_url"] + f"action=insert&attributes=%5B%7B%22value_name%22%3A%22dateObserved%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22timestamp%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22timestamp%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%2C%7B%22value_name%22%3A%22value44%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22message%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22-%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%5D&id={device_name}&type={conf['model']['model_type']}&kind={conf['model']['model_kind']}&contextbroker={conf['model']['model_contextbroker']}&format={conf['model']['model_format']}&mac=&model={get_latest_model()}&producer=&latitude={lat}&longitude={long}&visibility=&frequency={conf['model']['model_frequency']}&token={token}&k1=ae402872-8207-4451-83cb-d047a2f68340&k2=ecb6a002-8452-4f90-88d7-e0c4c4dcf370&edgegateway_type=&edgegateway_uri=&subnature={conf['model']['model_subnature']}&static_attributes=%5B%5D&service=&servicePath=&nodered=true"
    response = requests.request("PATCH", url, headers=header)
    r = (response.text)
    r = json.loads(r)
    print(f"\nStatus for device {get_latest_device()}: " + r['status'])
    time.sleep(2)
    
def getDevice(conf, device_name, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    url = conf["base-url"] + '/ownership-api/v1/list/?type=IOTID&accessToken='+token

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Request was successful: received the devices")
        data=response.json()

    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)
        
    desired_element = None
    for element in data:
        if element['elementName'] == device_name:
            desired_element = element
            print("Device was found")
            break
    return desired_element    

def accessTokenDelegated(conf):
    access_token = ''
    payload = {
        'f': 'json',
        'client_id': conf.get('token').get('clientID'),
        'grant_type': 'password',
        'username': conf["usernamedelegated"],
        'password': conf["usernamedelegatedpassword"]
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
        print(currentTime, "Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print(currentTime, "Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print(currentTime, "Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print(currentTime, "Ops: Something Else", err)
    else:
        token = response.json()
        access_token = token['access_token']

    return access_token

    
def delegateDevice(device_name, conf, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    device=getDevice(conf, device_name, token)  

    # Estrai i valori
    contextbroker = device['elementDetails']['contextbroker']
    k1 = device['elementDetails']['k1']
    k2 = device['elementDetails']['k2']

    url = conf["base-url"] + '/iot-directory/api/device.php?action=add_delegation&id='+device_name+'&delegated_user='+conf["usernamedelegated"]+'&contextbroker='+contextbroker+'&k1=' + k1 +'&k2=' + k2 +'&token=' + token +"&nodered=yes"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request was successful: device was delegated")
        #print("------------------------------------------------------------------------------------------------")
        #print("Response:")
        #print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)
        
    return device['elementUrl']
    
def deletedevice(device_name, context_broker, access_token, base_uri):
    header = {
        "Content-Type": "application/json",
        "Accept": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}",
    }
    url = base_uri + "?action=delete&id=" + device_name + "&contextbroker=" + context_broker + "&token=" + access_token + "&nodered=yes"
    response = requests.request("POST", url, headers=header)
    if (response.status_code == 200):
        print(f"\nDevice {device_name} deleted successfully")
    elif (response.status_code == 401):
        print("\nUnauthorized, accessToken: " + access_token)
    else:
        print("\nSomething else went wrong: " + response.content)
    

def sendData(conf, token, device_name, string_value):
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    timestamp = datetime.now().isoformat()
    timestamp = timestamp[0:20] + "000Z"
    payload = {"value44":{"type":"string","value": string_value},"dateObserved":{"type":"string","value":timestamp}}
    # http://dashtest/orion-filter-orion-1/v2/entities/20231120T094406device/attrs?elementid=20231120T094406device&type=test
    url = f'{conf["base-url"]}/orion-filter/orion-1/v2/entities/' + device_name + '/attrs?elementid=' + device_name + '&type=' + conf['model']['model_type']
    print(url)
    response = requests.request("PATCH", url, data=json.dumps(payload), headers=header)
    if (response.status_code == 204):
        print("Insert Succeded")
    else:
        print("Insert Failed")

def accessToken(conf):
    access_token = ''
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

    urlToken = conf.get('token').get('token_url')
    currentTime = datetime.now()
    try:
        response = requests.request("POST", urlToken, data=payload, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(currentTime, "Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print(currentTime, "Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print(currentTime, "Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print(currentTime, "Ops: Something Else", err)
    else:
        token = response.json()
        access_token = token['access_token']
    return access_token

def get_latest_device():
    with open('latest-device.txt', 'r') as f:
        return f.read()
        
def get_latest_model():
    with open('latest-model.txt', 'r') as f:
        return f.read()

if __name__ == "__main__":
    main()