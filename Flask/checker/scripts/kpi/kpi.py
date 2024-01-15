from datetime import datetime
import time
import json
import os
import requests
import time
import requests
import sys

broker_name="orion-1"
username = ""
password = ""
variable="value44"
try:
    username=sys.argv[1]
    password=sys.argv[2]
except Exception as E:
    print("Operation failed due to",E)
    exit(1)

def main():
    root_path = os.getcwd()
    params_path = root_path + "/data/conf.json"
    f = open(params_path)
    conf= json.load(f)
    print("Configuration file opened")
    access_token = accessToken(conf)
    idKpi=createKpi(conf,access_token)
    sendDataKpi(idKpi,conf,access_token)
    getKpi(idKpi,conf,access_token)


def getKpi(idKpi,conf, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["url"] + '/datamanager/api/v1/kpidata/'+str(idKpi)+'/values/?sourceRequest=iotapp&highLevelType=MyKPI"'

    data = {
        "kpiId": idKpi,
        "value": 30,
        "dataTime": int(time.time() * 1000)
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request was successful.")
        print("Response:")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)

def sendDataKpi(idKpi,conf, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = conf["url"] + '/datamanager/api/v1/kpidata/'+str(idKpi)+'/values/?sourceRequest=iotapp'

    data = {
        "kpiId": idKpi,
        "value": 30,
        "dataTime": int(time.time() * 1000)
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful.")
        print("Response:")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
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
        print("Request was successful.")
        print("Response:")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)

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


if __name__ == "__main__":
    main()
