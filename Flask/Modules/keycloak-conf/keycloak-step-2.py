import requests

KEYCLOAK_URL = '$#base-url#$/auth'
REALM_NAME = 'master'
CLIENT_ID = 'admin-cli'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '$#keycloak-admin-pwd#$'
ROLE_NAME = 'offline_access'
CLIENT_SCOPE_NAME = 'client_scope'

def get_access_token():
    token_url = f'{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'
    data = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']
	
def get_users(access_token):
    users_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(users_url, headers=headers)
    response.raise_for_status()
    return response.json()
	
def get_offline_access_role(access_token):
    roles_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/roles/{ROLE_NAME}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(roles_url, headers=headers)
    response.raise_for_status()
    return response.json()
	
def assign_role_to_user(access_token, user_id, role):
    user_roles_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users/{user_id}/role-mappings/realm'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(user_roles_url, headers=headers, json=[role])
    print(response)
	
try:
    token = get_access_token()
    users = get_users(token)
    role = get_offline_access_role(token)
    for user in users:
        print(user)
        assign_role_to_user(token, user['id'], role)
        print(f"Assigned offline_access role to user {user['username']}")
except Exception as e:
    print("An error occurred:", str(e))
	
def client_scope_exists(access_token):
    scopes_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/client-scopes'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(scopes_url, headers=headers)
    response.raise_for_status()
    client_scopes = response.json()
    for scope in client_scopes:
        if scope['name'] == CLIENT_SCOPE_NAME:
            return scope['id']
    return None
	
def create_client_scope(access_token):
    scopes_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/client-scopes'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    client_scope_data = {
        'name': CLIENT_SCOPE_NAME,
        'protocol': 'openid-connect'
    }
    response = requests.post(scopes_url, headers=headers, json=client_scope_data)
    response.raise_for_status()
    return response.json()['id']
	
def make_client_scope_default(access_token, client_scope_id):
    default_client_scopes_url = f'{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/default-default-client-scopes/{client_scope_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(default_client_scopes_url, headers=headers)
    response.raise_for_status()
	
try:
    token = get_access_token()
    client_scope_id = client_scope_exists(token)
    if not client_scope_id:
        client_scope_id = create_client_scope(token)
        print("Client scope created successfully")
    else:
        print("Client scope already exists")

    # Make the client scope default
    make_client_scope_default(token, client_scope_id)
    print("Client scope set as default successfully")
except Exception as e:
    print("An error occurred:", str(e))