#!/usr/bin/python3

import urllib.request
import urllib.parse
import json
import sys
import os

# CD to the script's directory
os.chdir( sys.path[0] )
# print( os.getcwd() )

usage_msg = "Usage:\n\tpython3 keycloak-rest.py <KEYCLOAK_URL> \n\nExamples: \n\tpython3 keycloak-rest.py http://dashboard/auth [username] [password]\n\tpython3 keycloak-rest.py http://snap4city-host:8088/auth"

if len(sys.argv) == 1:
	print( "No arguments provided.\n\n" + usage_msg )
	sys.exit()

if len(sys.argv) > 1:
	if sys.argv[1] == "help":
		print( usage_msg )
		sys.exit()
	else:
		keycloak_host = sys.argv[1]

username='admin'
password='$#keycloak-admin-pwd#$'
if len(sys.argv) > 2:
        username = sys.argv[2]
if len(sys.argv) > 3:
        password = sys.argv[3]

if not keycloak_host.endswith("/"):
	keycloak_host = keycloak_host + "/"

print( "Configuring Keycloak at:\n\t" + keycloak_host + " user:" + username + " pwd:" + password )

keycloak_token_endpoint = keycloak_host + 'realms/master/protocol/openid-connect/token'
keycloak_components_endpoint = keycloak_host + 'admin/realms/master/components'
keycloak_client_scopes_endpoint = keycloak_host + 'admin/realms/master/client-scopes'
keycloak_clients_endpoint = keycloak_host + 'admin/realms/master/clients'
keycloak_identity_providers_endpoint = keycloak_host + 'admin/realms/master/identity-provider/instances'
keycloak_auth_flow_endpoint = keycloak_host + 'admin/realms/master/authentication/flows'
keycloak_auth_exec_endpoint = keycloak_host + 'admin/realms/master/authentication/executions'
keycloak_realm_endpoint = keycloak_host + 'admin/realms/master'

# Utility function to perform HTTP requests
def perform_request( url , method=None , access_token=None , headers={} , data=None , data_type='form' ):
    if access_token is not None:
        headers['Authorization'] = 'Bearer ' + access_token

    if data is not None:
        if data_type == 'form':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            encoded_data = urllib.parse.urlencode(data).encode("ascii")
        elif data_type == 'json':
            headers['Content-Type'] = 'application/json;charset=UTF-8'
            encoded_data = json.dumps(data).encode("utf-8")
        else:
            raise ValueError("Invalid value for data_type='{0}'. Can be ['form','json']")
    else:
        encoded_data = None

    if method is None:
        req = urllib.request.Request(
            url , headers=headers , data=encoded_data
        )
    else:
        req = urllib.request.Request(
            url , headers=headers , data=encoded_data , method=method
        )

    with urllib.request.urlopen(req) as response:
        response_str = response.read().decode('utf-8')
        # print( "Response str: '" + response_str + "'" )
        if response_str:
            try:
                return json.loads( response_str )
            except json.decoder.JSONDecodeError as e:
                return response_str

# ----------------------------------------------------------------
# CONFIGURATION steps:

# 1 - ACCESS TOKEN
access_token_response = perform_request(
    keycloak_host + 'realms/master/protocol/openid-connect/token' ,
    data={
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': 'admin-cli'
    } ,
    data_type='form'
)
access_token = access_token_response['access_token']

# Get Realm Id
realm_response = perform_request(
    keycloak_host + 'admin/realms/master' ,
    access_token=access_token
)
realm_id = realm_response["id"]

# 2 - CREATE LDAP FEDERATION
with open('keycloak-conf-files/user-federation/LDAP_storage_provider.json','r') as file:
    ldap_storage_provider_conf = json.loads( file.read() )
ldap_storage_provider_conf["parentId"] = realm_id
perform_request(
    keycloak_host + 'admin/realms/master/components' ,
    access_token=access_token ,
    data=ldap_storage_provider_conf ,
    data_type='json'
)
print( "User federation 'ldap' created.")


# 3 - RETRIEVE LDAP STORAGE PROVIDER ID
ldap_provider_response = perform_request(
    keycloak_host + 'admin/realms/master/components?name=ldap&type=org.keycloak.storage.UserStorageProvider' ,
    access_token=access_token
)
ldap_storage_provider_id = ldap_provider_response[0]["id"]

# 4 - CREATE Mappers:
mappers_conf_files_dir = 'keycloak-conf-files/user-federation/mappers/'
for filename in os.listdir( mappers_conf_files_dir ):
    with open( mappers_conf_files_dir + filename , 'r' ) as file:
        mapper_conf = json.loads( file.read() )
        mapper_conf['parentId']=ldap_storage_provider_id
    perform_request(
        keycloak_components_endpoint ,
        access_token=access_token ,
        data=mapper_conf,
        data_type='json'
    )
    print( "\tMapper type='{0}' name='{1}' created.'".format(mapper_conf['providerId'] , filename[:len(filename)-5]) )


# 5 - SYNCHRONIZE
# retrieve role-ldap-mapper 'Manager' id
ldap_role_mapper_response=perform_request(
    keycloak_host + 'admin/realms/master/components?parent' + ldap_storage_provider_id + '&name=Manager',
    access_token=access_token
)
ldap_role_mapper_id = ldap_role_mapper_response[0]['id']

# trigger ROLES synchronization LDAP -> Keycloak
print(keycloak_host + 'admin/realms/master/user-storage/' + ldap_storage_provider_id +
                    '/mappers/' + ldap_role_mapper_id +
                    '/sync?direction=fedToKeycloak')
perform_request(
    keycloak_host + 'admin/realms/master/user-storage/' + ldap_storage_provider_id +
                    '/mappers/' + ldap_role_mapper_id +
                    '/sync?direction=fedToKeycloak' ,
    access_token=access_token ,
    method='POST'
)
print( "LDAP roles synchronized." )

# retrieve group-ldap-mapper 'Group Mapper' id
ldap_group_mapper_response=perform_request(
    keycloak_host + 'admin/realms/master/components?parent' + ldap_storage_provider_id + '&name=Group%20Mapper',
    access_token=access_token
)
ldap_group_mapper_id = ldap_group_mapper_response[0]['id']

# trigger GROUPS synchronization LDAP -> Keycloak
perform_request(
    keycloak_host + 'admin/realms/master/user-storage/' + ldap_storage_provider_id +
                    '/mappers/' + ldap_group_mapper_id +
                    '/sync?direction=fedToKeycloak' ,
    access_token=access_token ,
    method='POST'
)
print( "LDAP groups synchronized." )

# trigger USERS synchronization LDAP -> Keycloak
perform_request(
    keycloak_host + 'admin/realms/master/user-storage/' + ldap_storage_provider_id +
                    '/sync?action=triggerFullSync' ,
    access_token=access_token ,
    method='POST'
)
print( "LDAP users synchronized.")

# 6 - CREATE CLIENT SCOPES
client_scopes_conf_dir = "keycloak-conf-files/client-scopes/"
for filename in os.listdir( client_scopes_conf_dir ):
    try:
        with open( client_scopes_conf_dir + filename , 'r' ) as file:
            client_scope_conf = json.loads( file.read() )
        perform_request(
            keycloak_client_scopes_endpoint ,
            access_token=access_token ,
            data=client_scope_conf ,
            data_type='json'
        )
        print( "Client-scope '{0}' created.".format( filename[:len(filename)-5] ) )
    except:
        print( "FAILED Client-scope '{0}' creation.".format( filename[:len(filename)-5] ) )

# 7 - CREATE CLIENTS
client_conf_files_dir = "keycloak-conf-files/clients/"
for filename in os.listdir( client_conf_files_dir ):
    try:
        with open( client_conf_files_dir + filename , 'r' ) as file:
            client_conf = json.loads( file.read() )
        perform_request(
            keycloak_host + 'admin/realms/master/clients' ,
            access_token=access_token,
            data=client_conf ,
            data_type='json'
        )
        print( "Client '{0}' created.".format( filename[:len(filename)-5] ) )
    except:
        print( "FAILED Client '{0}' creation.".format( filename[:len(filename)-5] ) )

# 8 - DISABLE THE KEY PROVIDER FOR THE RSA-OAEP ALGORITHM
# (in order to return only one object from the certs endpoint:
# http://dashboard/auth/realms/master/protocol/openid-connect/certs )

# Get the key providers for the realm
key_providers = perform_request(
    keycloak_components_endpoint+"?parent=master&type=org.keycloak.keys.KeyProvider" ,
    access_token=access_token
)
# Filter the key providers to get "rsa-enc-generated"
target_key_provider = None
for key_provider in key_providers:
    if key_provider['name'] == 'rsa-enc-generated':
        target_key_provider = key_provider
        break
# Disable it if enabled
if target_key_provider:
    target_key_provider['config']['enabled']=['false']
    perform_request(
        keycloak_components_endpoint + "/" + target_key_provider['id'] ,
        access_token=access_token ,
        data=target_key_provider ,
        data_type='json',
        method='PUT'
    )
    print( "Key provider 'rsa-enc-generated' (RSA-OAEP algorithm) disabled." )

# 9 - CREATE AUTHENTICATION FLOW

try:
    # Copy "First Broker Login"
    perform_request(
	keycloak_auth_flow_endpoint + "/first%20broker%20login/copy" ,
	access_token=access_token ,
	data={ "newName" : "First Broker Login IdP" } ,
	data_type='json'
    )
    print( "Authentication Flow 'First Broker Login (IdP)' created" )

    # Create "Automatically Set Existing User" Execution
    perform_request(
	keycloak_auth_flow_endpoint + "/First%20Broker%20Login%20IdP%20Handle%20Existing%20Account/executions/execution" ,
	access_token=access_token ,
	data={ "provider" : "idp-auto-link" } ,
	data_type='json'
    )
    print( "'Automatically Set Existing User' Execution created" )

    # Get Execution
    flow_executions = perform_request(
	keycloak_auth_flow_endpoint + "/First%20Broker%20Login%20IdP/executions" ,
	access_token=access_token
    )
    auto_account_exec = next((x for x in flow_executions if x.get("providerId") == "idp-auto-link"), None)

    # Raise Execution Priority Twice
    perform_request(
	keycloak_auth_exec_endpoint + "/" + auto_account_exec["id"] + "/raise-priority" ,
	access_token=access_token ,
	method="POST"
    )
    perform_request(
	keycloak_auth_exec_endpoint + "/" + auto_account_exec["id"] + "/raise-priority" ,
	access_token=access_token ,
	method="POST"
    )
    print( "Raised priority of 'Automatically Set Existing User' Execution" )

    # Set Requirement for Multiple Executions
    auth_flow_conf_dir = "keycloak-conf-files/auth-flow-executions/"
    for filename in os.listdir( auth_flow_conf_dir ):
        with open( auth_flow_conf_dir + filename , 'r' ) as file:
            exec_conf = json.loads( file.read() )
        exec_el = next((x for x in flow_executions if exec_conf.get("providerId") != None and x.get("providerId") == exec_conf.get("providerId")), None)
        if exec_el != None:
            exec_conf["id"] = exec_el["id"]
        # One Execution doesn't have a "providerId", search by "displayName"
        else:
             exec_conf["id"] = next((x for x in flow_executions if x["displayName"] == "First Broker Login IdP Account verification options"), None)["id"]
        perform_request(
            keycloak_auth_flow_endpoint + "/First%20Broker%20Login%20IdP/executions" ,
            access_token=access_token ,
            data=exec_conf ,
            data_type='json' ,
            method="PUT"
        )
        print( "Execution '{0}' updated.".format( filename[:len(filename)-5] ) )
    print( "Authentication Flow 'First Broker Login (IdP)' configuration completed" )
except:
    print( "Authentication Flow 'First Broker Login (IdP)' configuration FAILED (already exists?)" )
print("not doing the last 2 steps because they don't work and they aren't needed")
exit(0)
# 10 - CREATE IDENTITY PROVIDERS
identity_providers_conf_dir = "keycloak-conf-files/identity-providers/"
idp_aliases = []
for filename in os.listdir( identity_providers_conf_dir ):
    if filename != 'mappers':
        try:
            with open( identity_providers_conf_dir + filename , 'r' ) as file:
                idp_conf = json.loads( file.read() )
            idp_aliases.append( idp_conf['alias'] )
            idp_conf["config"]["entityId"] = keycloak_host + "realms/master"
            perform_request(
                keycloak_identity_providers_endpoint ,
                access_token=access_token ,
                data=idp_conf ,
                data_type='json'
            )
            print( "Identity Provider '{0}' created.".format( filename[:len(filename)-5] ) )
        except:
            print( "FAILED Identity Provider '{0}' creation.".format( filename[:len(filename)-5] ) )

# 11 - CREATE MAPPERS FOR IDENTITY PROVIDERS
mappers_idp_conf_files_dir = 'keycloak-conf-files/identity-providers/mappers/'
for alias in idp_aliases:
    for filename in os.listdir( mappers_idp_conf_files_dir + alias ):
        try:
            with open( mappers_idp_conf_files_dir + alias + '/' + filename , 'r' ) as file:
                mapper_idp_conf = json.loads( file.read() )
            perform_request(
                keycloak_identity_providers_endpoint + '/' + alias + '/mappers' ,
                access_token=access_token ,
                data=mapper_idp_conf,
                data_type='json'
            )
            print( "\tMapper idp_alias='{0}' name='{1}' created.'".format(alias , filename[:len(filename)-5]) )
        except:
            print( "FAILED Mapper idp_alias='{0}' name='{1}' creation.'".format(alias , filename[:len(filename)-5]) )
