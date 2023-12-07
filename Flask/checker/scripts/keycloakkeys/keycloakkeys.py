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


import requests
import json

url = '$#base-url#$/auth/realms/master/protocol/openid-connect/certs'
try:
    response = requests.get(url)
    if response.status_code == 200:
        content = json.loads(response.text) 
        if len(content.keys())==1: #we want only one key to be here
            print("Works!")
        else:
            print(f"Error! {len(content.keys())} keys were found, only one was expected")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Error fetching the page: {e}")
