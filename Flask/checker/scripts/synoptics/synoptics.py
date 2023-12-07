'''Copyright (C) 2023 DISIT Lab http://www.disit.org - University of Florence

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.'''


import socketio
import requests
import json
import sys

http_session = requests.Session()
http_session.verify = False
sio = socketio.Client(logger=False, engineio_logger=False)



broker_name="orion-1"
username = ""
password = ""
device=""
variable="testValue"
try:
    username=sys.argv[1]
    password=sys.argv[2]
    device=sys.argv[3]
except Exception as E:
    print("Operation failed due to",E)
    exit(1)


def getTokenViaUserCredentials(username,password):
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

    urlToken = "$#base-url#$/auth/realms/master/protocol/openid-connect/token"
    response = requests.request("POST", urlToken, data=payload, headers=header)
    token = response.json()
    return token

@sio.event
def connect():
    print('establishing connection')
    token = getTokenViaUserCredentials(username, password)
    sio.emit("authenticate",token['access_token'])

@sio.event
def authenticate(data):
    print('authenticate result: ', data)
    jd = json.loads(data)
    if jd['status']=='OK' :
        sio.emit('subscribe','http://www.disit.org/km4city/resource/iot/orion-1/Organization/{device} {variable}')

@sio.event
def subscribe(data):
    print('subscribe result:', data)
    r = json.loads(data)
    if r['status'] == 'OK' :
      sio.on('update http://www.disit.org/km4city/resource/iot/orion-1/Organization/{device} {variable}', handle_update)

def handle_update(data):
    print(data)

@sio.event
def disconnect():
    print('disconnected from server')
    sio.disconnect()


sio.connect(url='$#base-url#$/',socketio_path='synoptics/socket.io',transports='websocket')
sio.wait()