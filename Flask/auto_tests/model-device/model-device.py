from datetime import datetime
import time
import json
import os

import requests


def main():
    root_path = os.getcwd()
    params_path = root_path + "/data/conf.json"
    f = open(params_path)
    config = json.load(f)
    print("Configuration file opened")
    access_token = accessToken(config)
    device_name = "deviceProva"+datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    createModel(config, access_token)
    with file('latest.txt', 'w') as f:
        f.write("deviceProva"+device_name)

    createDevice(config, access_token, device_name)

    nData = 10
    sleep = 2
    for i in range(0, nData):
        string_value = str(i)
        sendData(config, access_token, device_name, string_value)
        time.sleep(sleep)


def createModel(conf, token):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    this_moment=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    url = conf["model"]["model_url"] + f"action=insert&attributes=%5B%7B%22value_name%22%3A%22dateObserved%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22timestamp%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22timestamp%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%2C%7B%22value_name%22%3A%22value44%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22message%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22-%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%5D&name={get_latest()}"+this_moment+"&description=&type={conf['model']['model_type']}&kind={conf['model']['model_kind']}&producer=&frequency={conf['model']['model_frequency']}&kgenerator={conf['model']['model_kgenerator']}&edgegateway_type=&contextbroker={conf['model']['model_contextbroker']}&protocol={conf['model']['model_protocol']}&format={conf['model']['model_format']}&hc={conf['model']['model_hc']}&hv={conf['model']['model_hv']}&subnature={conf['model']['model_subnature']}&static_attributes=%5B%5D&service=&servicePath=&token={token}&nodered=false"
    response = requests.request("PATCH", url, headers=header)
    r = (response.text)
    r = json.loads(r)
    print(f"\nStato creazione modello {get_latest()}"+this_moment+": " + r['status'])
    time.sleep(2)

def createDevice(conf, token, device_name):

    long = "11.24657"
    lat = "43.77709"

    header = {
        "Content-Type": "application/json",
        "Accept": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}",
    }

    url = conf["device"]["device_url"] + f"action=insert&attributes=%5B%7B%22value_name%22%3A%22dateObserved%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22timestamp%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22timestamp%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%2C%7B%22value_name%22%3A%22value44%22%2C%22data_type%22%3A%22string%22%2C%22value_type%22%3A%22message%22%2C%22editable%22%3A%220%22%2C%22value_unit%22%3A%22-%22%2C%22healthiness_criteria%22%3A%22refresh_rate%22%2C%22healthiness_value%22%3A%22300%22%7D%5D&id={device_name}&type={conf['model']['model_type']}&kind={conf['model']['model_kind']}&contextbroker={conf['model']['model_contextbroker']}&format={conf['model']['model_format']}&mac=&model={get_latest()}&producer=&latitude={lat}&longitude=a{long}&visibility=&frequency={conf['model']['model_frequency']}&token={token}&k1=ae402872-8207-4451-83cb-d047a2f68340&k2=ecb6a002-8452-4f90-88d7-e0c4c4dcf370&edgegateway_type=&edgegateway_uri=&subnature={conf['model']['model_subnature']}&static_attributes=%5B%5D&service=&servicePath=&nodered=false"
    response = requests.request("PATCH", url, headers=header)
    r = (response.text)
    r = json.loads(r)
    print(f"\nStato creazione device {device_name} : " + r['status'])
    time.sleep(2)

def sendData(conf, token, device_name, string_value):

    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    timestamp = datetime.now().isoformat()
    timestamp = timestamp[0:20] + "000Z"
    payload = {"value44":{"type":"string","value": string_value},"dateObserved":{"type":"string","value":timestamp}}

    url = conf["patch"] + device_name + '/attrs?elementid=' + device_name + '&type=' + conf['model']['model_type']
    response = requests.request("PATCH", url, data=json.dumps(payload), headers=header)
    if (response.status_code == 204):
        print("\nInserimento riuscito")
    else:
        print("\nInserimento fallito")



def accessToken(conf):
    access_token = ''
    payload = {
        'f': 'json',
        'client_id': conf.get('token').get('clientID'),
        'client_secret': conf.get('token').get('clientSecret'),
        'grant_type': 'password',
        'username': conf.get('token').get('username'),
        'password': conf.get('token').get('password')
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
        print(currentTime, "OOps: Something Else", err)
    else:
        token = response.json()
        access_token = token['access_token']

    return access_token

def get_latest():
    with file('latest.txt', 'r') as f:
        return f.read()

if __name__ == "__main__":
    main()
