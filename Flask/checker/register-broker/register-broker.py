import datetime
import json

import requests


def accessToken(user, password):
    access_token = ''
    payload = {
        'f': 'json',
        'client_id': "php-ownership-api",
        'client_secret': "a347fb2d-87f0-4d41-89a9-b746b5273ccd",
        'grant_type': 'password',
        'username': user,
        'password': password
    }

    header = {
        'Content-Type': 'application/json'
    }

    urlToken = "$#base-url#$/auth/realms/master/protocol/openid-connect/token"
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


def main():
    json_payload={"token": accessToken("userrootadmin","Sl9.wrE@k"),
    "action": "update",
    "name": "orion-1",
    "kind": "internal",
    "path": "",
    "version": "v2",
    "visibility": "",
    "ip": "orion-001",
    "port": "1026",
    "protocol": "ngsi",
    "login": "login",
    "password": "login",
    "latitude": "$#lat-ib-0#$",
    "longitude": "$#lng-ib-0#$",
    "createdDate": "2024-01-11 09:21:42",
    "accesslink": "orion-broker-filter-001",
    "accessport": "8443",
    "apikey": "null",
    "sha": "",
    "urlnificallback": "http://nifi:1030/ingestngsi",
    "services": "[]",
    "log_orion": "0",
    }
    header={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    response=requests.request("POST", "$#base-url#$/iot-directory/api/contextbroker.php",headers=header,data=json.dumps(json_payload))
    print(response)
    return 0
    
if __name__ == "__main__":
    main()
