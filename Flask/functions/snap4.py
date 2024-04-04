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


import os, errno, shutil, copy
from copy import deepcopy
import re
import gzip

def make_iotapp_folder(origin, path, id_iotapp, placeholders):
    # make the folder and copy the files; do placeholders while at it
    os.makedirs(path+'/iotapp-'+str(id_iotapp).zfill(3))
    for dname, dirs, files in os.walk(origin):
        for file in files:
            copy(os.path.join(dname,file), os.path.join(path+'/iotapp-'+str(id_iotapp).zfill(3),file))
            with open(os.path.join(path+'/iotapp-'+str(id_iotapp).zfill(3),file)) as f:
                s = f.read()
                s=s.replace('$#nodered-id#$', 'iotapp-'+str(id_iotapp).zfill(3))
            for key, value in placeholders.items():
                s=s.replace(key, value)
            with open(os.path.join(path+'/iotapp-'+str(id_iotapp).zfill(3),file),'w') as f:
                f.write(s)
    return

def ensure_validity(placeholders, ips):
    if int(placeholders["# of IoT-Apps"]) > 1051:
        print("[LOG] Tried a configuration with too many iotapps.")
        return False
    if int(placeholders["# of IoT-Apps"]) < 1:
        print("[LOG] Tried a configuration with too few iotapps.")
        return False
    if '# of Iot-Brokers' in placeholders:
        if int(placeholders["# of Iot-Brokers"]) > 4:
            print("[LOG] Tried a configuration with too many iotbrokers.")
            return False
    if '# of ServiceMaps' in placeholders:
        if int(placeholders["# of ServiceMaps"]) > 4:
            print("[LOG] Tried a configuration with too many servicemaps.")
            return False
    if '# of Opensearch nodes' in placeholders:
        if int(placeholders["# of Opensearch nodes"]) > 4:
            print("[LOG] Tried a configuration with too many Opensearch Nodes.")
            return False
    if '# of Opensearch nodes' in placeholders:
        if int(placeholders["# of Opensearch nodes"]) < 1:
            print("[LOG] Tried a configuration with too few Opensearch Nodes.")
            return False
    if '# of IoT-Brokers' in placeholders:
        if int(placeholders["# of IoT-Brokers"]) < 1:
            print("[LOG] Tried a configuration with too few iotbrokers.")
            return False
    if '# of ServiceMaps' in placeholders:
        if int(placeholders["# of ServiceMaps"]) < 1:
            print("[LOG] Tried a configuration with too few servicemaps.")
            return False
    if '# of Virtuoso nodes' in placeholders:
        if int(placeholders["# of Virtuoso nodes"]) > 4:
            print("[LOG] Tried a configuration with too many Virtuoso Nodes.")
            return False
    if '# of Virtuoso nodes' in placeholders:
        if int(placeholders["# of Virtuoso nodes"]) < 1:
            print("[LOG] Tried a configuration with too few Virtuoso Nodes.")
            return False


    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    for ip in ips:
        match = ip_pattern.match(ip)
        if not match:
            print("[LOG] Found a missing IP")
            return False
    return True

# the amount of iot apps and their sockets are required
# sockets should have the length of iot_amount
# yes, you can probably compress the thing into 1 list
# reminder that triple quote is just another string format

def make_empty_apache(path, mode, iot_amount, first_socket, placeholders): #temporary solution to make empty apache
    with open(path, 'w') as f:
        f.write('')

def make_ngnix_micro(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://iotapp-$#nodered#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport).zfill(3))
    with open('./Modules/ngnix/nginx-micro.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'''\n}'''
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_micro_ssl(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://iotapp-$#nodered#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport).zfill(3))
    with open('./Modules/ngnix/nginx-micro.conf.ssl', 'r') as f:
        final_file=f.read()
    final_file=final_file.replace('#apps',iotapps)
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_normal_ssl(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://iotapp-$#nodered#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport).zfill(3))
    with open('./Modules/ngnix/nginx-normal.conf.ssl', 'r') as f:
        final_file=f.read()
    final_file=final_file.replace('#apps',iotapps)
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_normal(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://$#ip-1#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport+i).zfill(3))
    with open('./Modules/ngnix/nginx-normal.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+''''''+iotapps+'''\n}'''
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_small(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://$#ip-3#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport+i).zfill(3))
    with open('./Modules/ngnix/nginx-small.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'''
}'''
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_small_ssl(path, iot_amount, iotport, placeholders):
    iotapps=''
    for i in range(iot_amount):
        iotapps+='''
    location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://iotapp-$#nodered#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport).zfill(3))
    with open('./Modules/ngnix/nginx-small.conf.ssl', 'r') as f:
        final_file=f.read()
    final_file=final_file.replace('#apps',iotapps)
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcs(path, iot_amount, iotport, placeholders, servicamaps_amount):  #todo won't work as is
    iotapps=''
    servicemaps=''
    for i in range(iot_amount):
        iotapps+='''
        location /iotapp/iotapp-$#nodered#$/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_pass "http://$#ip-5#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
        }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport+i).zfill(3))
    for i in range(int(servicamaps_amount)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcs.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'\n}'+servicemaps
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcs_ssl(path, iot_amount, iotport, placeholders, servicamaps_amount):  #todo won't work as is
    iotapps=''
    servicemaps=''
    for i in range(iot_amount):
        iotapps+='''
            location /iotapp/iotapp-$#nodered#$/ {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_pass "http://$#ip-5#$:$#iotport#$/iotapp/iotapp-$#nodered#$/";
            }'''
        iotapps=iotapps.replace('$#nodered#$',str(i+1).zfill(3))
        iotapps=iotapps.replace('$#iotport#$',str(iotport+i).zfill(3))
    for i in range(int(servicamaps_amount)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://$#ip-4#$:'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcs.conf.ssl', 'r') as f:
        final_file=f.read()
    final_file=final_file.replace('#apps',iotapps)
    final_file=final_file.replace('#servicemap', servicemaps)
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcl(placeholders, path, iotapps_amount, iotapps_ips, servicemaps_ips, auth_ip, opensearch_master_ip, dashboard_ip, iotapp_port):
    iotapps=''
    for app_no in range(iotapps_amount):
        iotapps+='''
            location /iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/ {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_pass "http://'''+iotapps_ips[app_no%len(iotapps_ips)]+''':'''+str(iotapp_port+app_no)+'''/iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/";
            }'''
    servicemaps=''
    for i in range(len(servicemaps_ips)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcl.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'\n}'+servicemaps
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcl_ssl(placeholders, path, iotapps_amount, iotapps_ips, servicemaps_ips, auth_ip, opensearch_master_ip, dashboard_ip, iotapp_port):
    iotapps=''
    for app_no in range(iotapps_amount):
        iotapps+='''
            location /iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/ {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_pass "http://'''+iotapps_ips[app_no%len(iotapps_ips)]+''':'''+str(iotapp_port+app_no)+'''/iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/";
            }'''
    servicemaps=''
    for i in range(len(servicemaps_ips)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcl.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'\n}'+servicemaps
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcm(placeholders, path, iotapps_amount, iotapps_ips, servicemaps_ips, auth_ip, opensearch_master_ip, dashboard_ip, iotapp_port, orionfilterips):
    iotapps=''
    for app_no in range(iotapps_amount):
        iotapps+='''
            location /iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/ {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_pass "http://'''+iotapps_ips[app_no%len(iotapps_ips)]+''':'''+str(iotapp_port+app_no)+'''/iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/";
            }'''
    servicemaps=''
    for i in range(len(servicemaps_ips)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcm.conf', 'r') as f:
        final_file=f.read()
    final_file=final_file+iotapps+'\n}'+servicemaps
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def make_ngnix_dcm_ssl(placeholders, path, iotapps_amount, iotapps_ips, servicemaps_ips, auth_ip, opensearch_master_ip, dashboard_ip, iotapp_port, orionfilterips):
    iotapps=''
    for app_no in range(iotapps_amount):
        iotapps+='''
            location /iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/ {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_pass "http://'''+iotapps_ips[app_no%len(iotapps_ips)]+''':'''+str(iotapp_port+app_no)+'''/iotapp/iotapp-'''+str(app_no+1).zfill(3)+'''/";
            }'''
    servicemaps=''
    for i in range(len(servicemaps_ips)):  #todo mix port
        if i == 0:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }
        location  /superservicemap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/superservicemap/rest/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
        else:
            servicemaps+='''
server {
        listen 80;
        listen [::]:80;

        server_name $#servicemap-'''+str(i).zfill(3)+'''#$;

        location  /ServiceMap/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/ServiceMap/";
        }
        location  /ServiceMap/api/v1/iot/ {
            proxy_pass "http://'''+servicemaps_ips[i]+''':'''+str(8090+i)+'''/iot/";
        }


        rewrite ^/$ /ServiceMap/ redirect;
}'''
    with open('./Modules/ngnix/nginx-dcm.conf.ssl', 'r') as f:
        final_file=f.read()
    final_file=final_file.replace('#apps', iotapps)
    final_file=final_file.replace('#servicemap', servicemaps)
    os.makedirs(path)
    with open(path+'/nginx.conf','w') as f:
        f.write(final_file)
    placeholders_in_file(path+'/nginx.conf', placeholders)
    return

def remove_heatmap_mentions(path):
    with open(path, 'a') as f:
        f.write('''DELETE FROM Dashboard.MainMenuSubmenus WHERE id=169;
DELETE FROM Dashboard.MainMenuSubmenus WHERE id=277;
DELETE FROM Dashboard.MainMenuSubmenus WHERE id=278;
''')
    return

def make_iotapp_yaml(origin, path, iot_id, placeholders, socket):
    copy('./Modules/'+origin, path)  # assuming folders exist already
    os.rename(os.path.join(path)+origin,os.path.join(path)+'docker-compose-iotapp-'+str(iot_id).zfill(3)+'.yml')
    s=""
    with open(path+'docker-compose-iotapp-'+str(iot_id).zfill(3)+'.yml','r') as f:
        s = f.read()
        s=s.replace('$#nodered-id#$', str(iot_id).zfill(3))  # adjust app placeholder
        s=s.replace('1880:1880', str(socket)+':1880')  # adjust socket
    for key, value in placeholders.items():
        s=s.replace(key, value)
    with open(os.path.join(path,'docker-compose-iotapp-'+str(iot_id).zfill(3)+'.yml'),'w') as f:
        f.write(s)
# this is, for example, used because we need to regenerate the right section of the form for the placeholders
# currently not used
def retrieve_variable_components(source_dict):
    dict_to_ret = {}
    for key, value in source_dict.items():
        if 'nodered-' in key:
            if 'nodered-' in dict_to_ret:
                dict_to_ret['nodered-'] += 1
            else:
                dict_to_ret['nodered-'] = 1
        if 'IoT-Broker-' in key:
            if 'IoT-Broker-' in dict_to_ret:
                dict_to_ret['IoT-Broker-'] += 1
            else:
                dict_to_ret['IoT-Broker-'] = 1
    dict_to_ret['Model name']=source_dict['Model name']
    return dict_to_ret

def merge_yaml(directory):  #note: will output errors in console, if error happens leaves empty file
    if os.path.exists('/Flask'+directory[1:]+'/docker-compose.yml'):
        print('Skipping duplicate compose creation')
        return
    base = 'docker-compose '
    for root,subdirs,files in os.walk(directory):  # break to skip the subdirs
        files.sort()
        for file in files:
            if file.endswith(".yml"):
                base += '-f ' + file + ' '
        break

    base+= 'config'
    cmd = 'cd '+'/Flask'+directory[1:]+' ; '+base+' > docker-compose.yml'
    # docker offers a command to merge many .yml files at once, one by one
    # technically order matters, but all of our components only appear exactly once
    # and don't touch each other, so the order doesn't matter to us
    os.system(cmd)
    for root,subdirs,files in os.walk(directory):
        for file in files:
            if file!='docker-compose.yml' and file.endswith(".yml"):
                try:
                    pass
                    os.remove(os.path.join(directory,file))
                except Exception:
                    pass
        break
    adjust = ""
    try:
        with open(directory+'/docker-compose.yml', 'r') as yaml_file:
            adjust=yaml_file.read()
            adjust=re.sub('/Flask'+directory[1:]+'/','./', adjust)
        with open(directory+'/docker-compose.yml', 'w') as yaml_file:
            yaml_file.write(adjust)
    except FileNotFoundError as Error:
        print(directory, 'had no compose to merge.')
    return

def adjust_dashboard_menu_dump(iot_app_amount, add_checker=False): #make iotapps visible in dashboard menu
    if iot_app_amount == 0:
        return None
    str_to_add='DELETE FROM Dashboard.MainMenuSubmenus WHERE text LIKE "IoT Application nodered%";\n'
    str_to_add+='INSERT INTO Dashboard.MainMenuSubmenus (menu,linkUrl,linkid,icon,text,privileges,userType,externalApp,openMode,iconColor,pageTitle,menuorder,organizations) VALUES '
    for i in range(iot_app_amount):
        str_to_add+='''('''+str(1035)+''','$#base-protocol#$://$#base-hostname#$/iotapp/iotapp-'''+str(i+1).zfill(3)+'''/','iotapp-'''+str(i+1).zfill(3)+"','fa fa-file-code-o','IoT Application nodered "+str(i+1).zfill(3)+"','[\\'RootAdmin\\', \\'AreaManager\\']','any','yes','iframe','#FFFFFF','IoT Application nodered "+str(i+1).zfill(3)+'''', '''+str(i)+''', '[\\'Organization\\',\\'DISIT\\',\\'Other\\']'),\n'''
    if add_checker:
        str_to_add+='''('1035', '/iotapp/iotapp-001/ui/#!/0', 'sanity-components', 'fa fa-file-code-o', 'Check components', '[\\'RootAdmin\\']', 'any', 'yes', 'iframe', '#ffffff', 'Check components', '0', '*'),\n'''
        str_to_add+='''('1156', '/phpldapadmin/', 'myLDAP', 'fa fa-users', 'User Role Management', '''+"'[\\'RootAdmin\\']'"+''', 'any', 'yes', 'iframe', '#f44242', 'User Role Management', '3', '*'),\n'''
    #add superservicemap
    str_to_add = str_to_add[:-2]  # remove the last comma and new line
    str_to_add+=''';\nINSERT INTO `Dashboard`.`MainMenuSubmenus` (`id`, `menu`, `linkUrl`, `linkId`, `icon`, `text`, `privileges`, `userType`, `externalApp`, `openMode`, `iconColor`, `pageTitle`, `menuOrder`) VALUES ('10800', '1059', '/MultiServiceMap/', 'map1link21', 'fa fa-map', 'MultiServiceMap', "[\'RootAdmin\',\'ToolAdmin\', \'AreaManager\', \'Manager\', \'Public\']", 'any', 'any', 'iframe', '#20ff41', 'SuperServiceMap', '2');'''
    return str_to_add+adjust_dashboard_menu_for_filemanager()+add_file_model_definition()

def adjust_dashboard_menu_for_filemanager():
    str_to_add = '''\nINSERT INTO `Dashboard`.`MainMenuSubmenus` (`id`, `menu`, `linkUrl`, `linkId`, `icon`, `text`, `privileges`, `userType`, `externalApp`, `openMode`, `iconColor`, `pageTitle`, `menuOrder`, `organizations`) VALUES ('10245', '1095', '../management/filemanager.php', 'filemanager', 'fa fa-server', 'Filemanager', "[\'RootAdmin\', \'ToolAdmin\', \'AreaManager\', \'Manager\']", 'any', 'yes', 'iframe', '#66ee22', 'FileManager', '100', '*');'''
    # INSERT INTO `Dashboard`.`MainMenuSubmenus` values (277,1095,'https://processloader.snap4city.org/management/filemanager.php',NULL,'psLink2hh','fa fa-download','Filemanager','[\'*\']','any','yes','iframe','#41b5f4','Filemanager',7,'')
    return str_to_add

def add_file_model_definition():
    str_to_add = '''\nINSERT INTO `iotdb`.`model` (`id`, `name`, `description`, `devicetype`, `kind`, `producer`, `frequency`, `attributes`, `contextbroker`, `protocol`, `format`, `healthiness_criteria`, `healthiness_value`, `kgenerator`, `edgegateway_type`, `organization`, `visibility`, `subnature`, `static_attributes`) VALUES ('2', '', 'fileModel', 'file', 'sensor', 'DISIT', '600', '[{\"value_name\":\"dateObserved\",\"data_type\":\"string\",\"value_type\":\"timestamp\",\"editable\":\"0\",\"value_unit\":\"timestamp\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"originalfilename\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"newfileid\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"language\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"description\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"filesize\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"},{\"value_name\":\"filetype\",\"data_type\":\"string\",\"value_type\":\"description\",\"editable\":\"0\",\"value_unit\":\"text\",\"healthiness_criteria\":\"refresh_rate\",\"healthiness_value\":\"300\"}]', 'orion-1', 'ngsi', 'json', 'refresh_rate', '300', 'normal', '', 'Organization', 'public', '', '[]');'''
    return str_to_add

def adjust_profiledb_dump(iot_app_amount): # assigns iotapps to user (defaults to user area manager)
    if iot_app_amount == 0:
        return None
    str_to_add='INSERT INTO profiledb.`ownership` VALUES '
    for i in range(iot_app_amount):
        str_to_add+='''("'''+str(i+1)+'''",'userareamanager',"'''+'iotapp-'+str(i+1).zfill(3)+'''",'AppID','nodered','http://$#base-hostname#$/iotapp/'''+str(i+1).zfill(3)+'''/','{\"edgegateway_type\":\"linux_Linux_4.9.0-8-amd64\"}',NULL,'2019-02-19 09:15:00',NULL,NULL),'''
    str_to_add = str_to_add[:-1]  # remove the last comma
    str_to_add+=';\n'
    return str_to_add

def placeholders_in_file(file_path, placeholders): #replace all placeholders with desired values
    s = ""
    with open(file_path, 'r') as file_opened:
        s=file_opened.read()
    for key, value in placeholders.items():
        s=s.replace(key, value)
    with open(file_path, 'w') as file_opened:
        file_opened.write(s)

def make_sql_micro(file_location, broker_ip, iotapps, broker_data, add_checker=True):
    #filemanager stuff
    filemanagerstring = ""
    with open("./Modules/database/filemanager.sql", 'r') as filemanagerstuff:
        filemanagerstring = filemanagerstuff.read()
    with open(file_location, 'w') as f:
        data=[]
        data.append('DELETE FROM profiledb.`ownership`;\n') # clean ownership
        data.append(adjust_profiledb_dump(iotapps))
        data.append(adjust_dashboard_menu_dump(iotapps, add_checker))
        brokers = iotbroker_add(broker_ip,broker_data)
        data.append(brokers[0])
        data.append(brokers[1])
        data.append('''
UPDATE Dashboard.MainMenu SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.MainMenuSubmenus SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.Domains SET domains=replace(domains,"dashboard","$#base-hostname#$");
UPDATE Dashboard.Organizations SET kbURL=replace(kbURL,"http://dashboard/","$#base-url#$/");
UPDATE Dashboard.MainMenuSubmenus SET `privileges` = "[\'RootAdmin\',\'ToolAdmin\',\'AreaManager\',\'Manager\']" WHERE (`id` = '10206');
DELETE FROM Dashboard.MainMenuSubmenus WHERE ID=277;
DELETE FROM Dashboard.MainMenu WHERE ID=2004;

''')
        for element in data:
            if element is not None:
                f.write(element)
        f.write('\n' + filemanagerstring)
    return

def adjust_dashboard_menu_dump_servicemaps(amount_of_servicemaps, path, fine_as_is):
    str_to_add='DELETE FROM Dashboard.MainMenuSubmenus WHERE ID=800;\n'
    str_to_add+='INSERT INTO Dashboard.MainMenuSubmenus VALUES '
    for i in range(int(amount_of_servicemaps)):
        str_to_add+='''({},{},'http://{}/',NULL,'{}','	fa fa-map','{}',"[\'RootAdmin\',\'ToolAdmin\', \'AreaManager\', \'Manager\', \'Public\']",'any','yes','iframe','#41f497','{}',{},'*'),'''.format(10906+i,1059,'$#servicemap-'+str(i).zfill(3)+'#$/ServiceMap','servicemap-'+str(i+1).zfill(3),'Service Map '+str(i+1), 'Service Map '+str(i+1),str(i+1))
    str_to_add = str_to_add[:-1]  # remove the last comma
    str_to_add+=';\n'
    with open(path,'a') as f:
        f.write(str_to_add)
    return

def fix_coordinates_micro(amount_of_servicemaps, path, fine_as_is):
    str_to_add='DELETE FROM Dashboard.Organizations;\n'
    str_to_add+='INSERT INTO Dashboard.Organizations VALUES '
    for i in range(int(amount_of_servicemaps)):
        # (7,'Organization','http://dashboard/ServiceMap/api/v1/','43.77251027974299,11.260920094643383',13,'eng','','','','http://virtuoso-kb:8890','','',' ','userareamanager',NULL)
        str_to_add+='''({},'Organization','$#base-url#$/ServiceMap/api/v1/','$#lat-ib-0#$,$#lng-ib-0#$','$#zoom-0#$','eng','','','','http://virtuoso-kb:8890','','',' ','userareamanager',NULL),'''.format(7+i)
    str_to_add = str_to_add[:-1]  # remove the last comma
    str_to_add+=';\n'
    with open(path,'a') as f:
        f.write(str_to_add)
    return

def make_sql_normal(file_location, broker_ip, iotapps, broker_data, add_checker=True):
    return make_sql_micro(file_location, broker_ip, iotapps, broker_data, add_checker)

def make_sql_small(file_location_1, file_location_2, broker_ip, iotapps, broker_data):
    filemanagerstring = ""
    with open("./Modules/database/filemanager.sql", 'r') as filemanagerstuff:
        filemanagerstring = filemanagerstuff.read()
    brokers = iotbroker_add(broker_ip,broker_data)
    with open(file_location_1, 'w') as f:
        data=[]
        data.append('DELETE FROM profiledb.`ownership`;\n') # clean ownership
        data.append(adjust_profiledb_dump(iotapps))
        data.append(adjust_dashboard_menu_dump(iotapps))
        data.append(brokers[0])
        data.append(brokers[1])

        data.append('''
UPDATE Dashboard.MainMenu SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.MainMenuSubmenus SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.Domains SET domains=replace(domains,"dashboard","$#base-hostname#$");
UPDATE Dashboard.Organizations SET kbURL=replace(kbURL,"http://dashboard/","$#base-url#$/");
UPDATE Dashboard.MainMenuSubmenus SET `privileges` = '[\'RootAdmin\',\'ToolAdmin\',\'AreaManager\',\'Manager\']' WHERE (`id` = '10206');

''')
        for element in data:
            if element is not None:
                f.write(element)
        f.write('\n' + filemanagerstring)
    return

def make_sql_dcs(file_location_1, file_location_2, broker_ip, iotapps, broker_data):
    return make_sql_small(file_location_1, file_location_2, broker_ip, iotapps, broker_data)

def make_sql_dcm(file_location_1, file_location_2, broker_ips, iotapps, broker_data):
    return make_sql_dcl(file_location_1, file_location_2, broker_ips, iotapps, broker_data)

def make_sql_dcl(file_location_1, file_location_2, broker_ips, iotapps, broker_data):
    brokers = iotbroker_add_multi(broker_ips, broker_data)
    with open(file_location_1, 'w') as f:
        data=[]
        data.append('DELETE FROM profiledb.`ownership`;\n') # clean ownership
        data.append(adjust_profiledb_dump(iotapps))
        data.append(adjust_dashboard_menu_dump(iotapps))
        data.append(brokers[0])
        data.append(brokers[1])

        data.append('''
UPDATE Dashboard.MainMenu SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.MainMenuSubmenus SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.Domains SET domains=replace(domains,"dashboard","$#base-hostname#$");
UPDATE Dashboard.Organizations SET kbURL=replace(kbURL,"http://dashboard/","$#base-url#$/");
UPDATE Dashboard.MainMenuSubmenus SET `privileges` = "[\'RootAdmin\',\'ToolAdmin\',\'AreaManager\',\'Manager\']" WHERE (`id` = '10206');

''')
        for element in data:
            if element is not None:
                f.write(element)
    data=[]
    return

def make_iotb_data(fine_as_is):
    iotb_data=[]
    try:
        i=0
        while True: # eventually we are gonna run out of data
            iotb_data.append([fine_as_is['$#lat-ib-'+str(i)+'#$'],fine_as_is['$#lng-ib-'+str(i)+'#$']])
            i+=1
    except:
        return iotb_data

def make_multiple_brokers(iot_broker_amount, path, yml, placeholders):
    for i in range(int(iot_broker_amount)):
        copy('./Modules/orionbrokerfilter-conf', path+'/orionbrokerfilter-'+str(i+1).zfill(3)+'-conf')
        copy('./Modules/orionbrokerfilter-logs', path+'/orionbrokerfilter-'+str(i+1).zfill(3)+'-logs')
        copy('./Modules/'+yml, path+'/docker-compose-iotobsf-'+str(i+1).zfill(3)+'.yml')
        with open(path+'/docker-compose-iotobsf-'+str(i+1).zfill(3)+'.yml','r') as f:
            s=f.read()
        s=s.replace('$#orion-id#$',str(i+1).zfill(3))
        s=s.replace('$#1026#$',str(1026+i))
        s=s.replace('$#8443#$',str(8443+i))
        s=s.replace('$#org_id#$',str(i+1))
        with open(path+'/docker-compose-iotobsf-'+str(i+1).zfill(3)+'.yml','w') as f:
            f.write(s)
        placeholders_in_file(path+'/docker-compose-iotobsf-'+str(i+1).zfill(3)+'.yml',placeholders)
        post_setup_obf(path, i)

    return

def post_setup_obf(path, id, file_to_append='post-setup.sh'):
    with open('./Modules/post-setup-obf.sh','r') as f:
        s=f.read()
    s=s.replace('$#orion-id#$',str(id+1).zfill(3))
    with open(path+'/'+file_to_append,'a') as f:
        f.write(s)

def make_nifi_conf(path, iotbrokers, placeholders):
    if iotbrokers<10 and iotbrokers>2:
        iotbrokers=10
    with gzip.open(path, 'w') as f_1:
        if '$#servicemap-000#$' not in placeholders:
            placeholders['$#servicemap-000#$'] = placeholders['$#base-hostname#$']
        if '$#servicemap-001#$' not in placeholders:
            placeholders['$#servicemap-001#$'] = placeholders['$#base-hostname#$']
        with open('./Modules/nifi/conf/flow.xml', 'r') as f_2:
            data=f_2.read()
            for i in range(int(iotbrokers)):
                data=data.replace('$#port-'+str(i+1)+'#$',str(1030+i))
            for key, value in placeholders.items():
                data=data.replace(key, value)
            f_1.write(data.encode('utf8'))
    return

def fix_service_map_config(file_path, replacing_string):
    s = ""
    with open(file_path, 'r') as file_opened:
        s=file_opened.read()
    s=s.replace('virtuoso-kb-$#servicemap-id#$',replacing_string)
    with open(file_path, 'w') as file_opened:
        file_opened.write(s)
    return

def merge_sh(file_path, files_to_merge):
    s = ""
    for item in files_to_merge:
        try:
            with open(item, 'r') as file_opened:
                s+=file_opened.read()
            os.remove(item)
        except Exception as E:
            print("[WARN]",item,"was not found, the file wasn't merged.")
    with open(file_path, 'a') as file_opened:
        file_opened.write(s)
    return

def make_n_servicemaps(amount_of_servicemaps, path, placeholders,start=0):
    temp_placeholders={}
    try:
        os.makedirs(path+'/database/')
    except FileExistsError as E:
        print('skipping folder creation')
    sql=make_servicemap_sql(int(amount_of_servicemaps))
    for i in range(int(amount_of_servicemaps)):
        temp_sql=deepcopy(sql)
        temp_sql.pop(i)
        copy('./Modules/servicemap-conf', path+'/servicemap-'+str(i+1+start).zfill(3)+'-conf')
        copy('./Modules/servicemap-iot-conf', path+'/servicemap-'+str(i+1+start).zfill(3)+'-iot-conf')
        copy('./Modules/servicemap-superservicemap-conf', path+'/servicemap-'+str(i+1+start).zfill(3)+'-superservicemap-conf')
        copy('./Modules/docker-compose-kbssm-city-small.yml', path+'/docker-compose-kbssm-city-small-'+str(i+1+start).zfill(3)+'.yml')
        update_ontology_sh(path+'/servicemap-'+str(i+1+start).zfill(3)+'-conf/update-ontology.sh', str(i+8890), 'virtuoso-kb-'+str(i+1+start).zfill(3))
        fix_servicemap_properties(path+'/servicemap-'+str(i+1+start).zfill(3)+'-conf/servicemap.properties', placeholders, str(i+8890+start),str(i+1111+start), str(i+3306+start),str(8983+i+start),str(i+1+start).zfill(3))
        copy('./Modules/docker-compose-db-datacitysmall-5.yml', path+'/docker-compose-db-datacitysmall-5-'+str(i+1+start).zfill(3)+'.yml')
        copy('./Modules/database/servicemap.sql', path+'/database/servicemap.sql')
        copy('./Modules/database/superservicemap.sql', path+'/database/superservicemap.sql')
        temp_placeholders['$#id#$']=str(i+1+start).zfill(3)
        temp_placeholders['$#8890#$']=str(8890+i)
        temp_placeholders['$#1111#$']=str(1111+i)
        temp_placeholders['$#8090#$']=str(8090+i)
        temp_placeholders['$#3306#$']=str(3306+i)
        temp_placeholders['$#8983#$']=str(8983+i)
        placeholders_in_file(path+'/docker-compose-kbssm-city-small-'+str(i+1+start).zfill(3)+'.yml',temp_placeholders)
        placeholders_in_file(path+'/docker-compose-db-datacitysmall-5-'+str(i+1+start).zfill(3)+'.yml',temp_placeholders)
        with open(path+'/database/superservicemap_additional-'+str(i+1+start).zfill(3)+'.sql', 'w') as f:
            for elem in temp_sql:
                f.write(elem)
        placeholders_in_file(path+'/database/superservicemap_additional-'+str(i+1+start).zfill(3)+'.sql',placeholders)
    for dname, dirs, files in os.walk(path):
        for file in files:
            try:
                placeholders_in_file(os.path.join(dname,file),placeholders)
            except UnicodeDecodeError as E:
                print('replacing in wrong file failed but everything is fine')
    return

def update_ontology_sh(path, port, virtuoso_name):
    data=''
    with open(path,'r') as f:
        data=f.read()
    data=data.replace('8890', port)
    data=data.replace('virtuoso-kb', virtuoso_name)
    with open(path,'w') as f:
        f.write(data)
    return

def fix_servicemap_properties(path, placeholders, port_1, port_2, port_3, port_4, identifier):
    data=''
    with open(path,'r') as f:
        data=f.read()
    data=data.replace('$#servicemap-id#$',identifier)
    data=data.replace('8890', port_1)
    data=data.replace('1111', port_2)
    data=data.replace('3306', port_3)
    data=data.replace('8983', port_4)
    data=data.replace('$#base-url#$','$#base-protocol#$://$#ip-0#$')
    data=data.replace('$#servicemap-db-host#$','dashboarddb-'+identifier)
    data=data.replace('virtuoso-kb:','virtuoso-kb-'+identifier+':')
    data=data.replace('solr-kb','solr-kb-'+identifier+':')
    data=data.replace('/ServiceMap/','/$#servicemap-'+identifier+'#$/')

    with open(path,'w') as f:
        f.write(data)
    return

def make_ldif_multi(path, file_name, how_many):
    with open('./Modules/ldap/default_multi.ldif', 'r') as source:
        output = ''
        for i in range(how_many):
            base = source.read()
            base=base.replace('$#number#$',str(i+6000))
            base=base.replace('$#iotbroker#$','orion-'+str(i))
            output+=base
        os.makedirs(path, exist_ok=True)
        with open(path+'/default.ldif', 'w') as result:
            result.write(output)

    copy('./Modules/ldap/psw_update.ldif', path+'/psw_update.ldif')

    return

def make_ldif(path, file_name, number, name_organizations, amount=1):  #
    try:
        copy('./Modules/ldap/default_'+str(amount)+'.ldif', path+'/'+file_name)

    except IOError as e:
    # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(path)
        copy('./Modules/ldap/default_'+str(amount)+'.ldif', path+'/'+file_name)

    copy('./Modules/ldap/default_'+str(amount)+'.ldif', path+'/'+file_name)
    copy('./Modules/ldap/psw_update.ldif', path+'/psw_update.ldif')


    with open(path+'/'+file_name, 'r') as file_opened:
        s=file_opened.read()
    if amount==1:
        s=s.replace('$#number#$',number[0])
        s=s.replace('$#iotbroker#$', name_organizations[0])
    elif amount==2:
        s=s.replace('$#number_1#$',number[0])
        s=s.replace('$#iotbroker_1#$', name_organizations[0])
        s=s.replace('$#number_2#$',number[1])
        s=s.replace('$#iotbroker_2#$', name_organizations[1])
    else:
        print('something failed')
        return
    with open(path+'/'+file_name, 'w') as file_opened:
        file_opened.write(s)
    return

def iotbroker_add_multi(broker_urls, broker_coords): #TODO remove iotbsf hardcoding  #TODO fix when nifi is away
    ownership='''INSERT INTO profiledb.`ownership` (`username`, `elementId`, `elementType`, `elementName`, `elementUrl`) values'''
    i=0
    for broker in broker_coords:  # i adjusts the broker name as it is in docker compose
        i+=1
        ownership+="('userrootadmin', 'Organization:orion-"+str(i)+"','BrokerID','Organization:orion-"+str(i)+"','"+'iotbsf'+"'),"
    ownership=ownership[:-1]+';\n'
    contextbroker='''INSERT INTO iotdb.`contextbroker` (`name`, `protocol`, `ip`, `port`, `uri`, `login`, `password`, `latitude`, `longitude`, `accesslink`, `accessport`, `sha`, `organization`, `apikey`, `visibility`, `version`, `path`, `kind`, `subscription_id`, `urlnificallback`) values'''
    i=0
    for broker in broker_coords:
        contextbroker+="('orion-"+str(i+1)+"','ngsi','"+broker_urls[i]+"','1026',NULL,'login','login','"+str(broker_coords[i][0])+"','"+str(broker_coords[i][1])+"','"+broker_urls[i]+"','"+str(8443+i)+"','','Organization',NULL,'private', 'v2', '', 'internal', 'register', 'http://nifi:1030/ingestngsi'),"
        i+=1
    contextbroker=contextbroker[:-1]+';\n'
    return [ownership,contextbroker]

def iotbroker_add(broker_url, broker_coords): #TODO remove iotbsf hardcoding  #TODO fix when nifi is away
    ownership='''INSERT INTO profiledb.`ownership` (`username`, `elementId`, `elementType`, `elementName`, `elementUrl`) values'''
    i=0
    for broker in broker_coords:  # i adjusts the broker name as it is in docker compose
        i+=1
        ownership+="('userrootadmin', 'Organization:orion-"+str(i)+"','BrokerID','Organization:orion-"+str(i)+"','"+'iotbsf'+"'),"
    ownership=ownership[:-1]+';\n'
    contextbroker='''INSERT INTO iotdb.`contextbroker` (`name`, `protocol`, `ip`, `port`, `uri`, `login`, `password`, `latitude`, `longitude`, `accesslink`, `accessport`, `sha`, `organization`, `apikey`, `visibility`, `version`, `path`, `kind`, `subscription_id`, `urlnificallback`) values'''
    i=0
    for broker in broker_coords:
        contextbroker+="('orion-"+str(i+1)+"','ngsi','orion-001','1026',NULL,'login','login','"+str(broker_coords[i][0])+"','"+str(broker_coords[i][1])+"','orionbrokerfilter-001','"+str(8443+i)+"','','Organization',NULL,'private', 'v2', '', 'internal', 'register', 'http://nifi:1030/ingestngsi'),"
        i+=1
    contextbroker=contextbroker[:-1]+';\n'
    return [ownership,contextbroker]
# in contextbroker
# 'iot-name', 'amqp', '192.168.1.55', '20630', NULL, 'login', 'login', '43.80877', '11.19919', '2021-07-18 10:30:29', 'dashboard', '20631', '', 'Organization', NULL, 'private', '5', '', 'internal', NULL, ''
# in ownership
# '16562', 'userrootadmin', 'Organization:iot-name', 'BrokerID', 'Organization:iot-name', 'dashboard', NULL, NULL, '2021-07-18 10:30:30', NULL, NULL
# 'dashboard' is supposed to be a string like 'iotobsf'

def make_servicemap_sql(how_many):
    total=[]
    for i in range(how_many):
        line='''INSERT INTO `SuperServiceMap`.`servicemaps` (`id`, `ip`, `competenceArea`, `urlPrefix`) VALUES ('{}', '192.168.1.121', 'POLYGON((-158.21469745574612 73.3570949908289,178.58217754425382 73.3570949908289,178.58217754425382 -59.303568590034,-158.21469745574612 -59.303568590034,-158.21469745574612 73.3570949908289))', 'http://{}:{}/ServiceMap');
'''.format('servicemap-'+str(i+1).zfill(3),'$#servicemap-'+str(i+1).zfill(3)+'#$',8090+i)
        total.append(line)
    return total

def fixvarnish(file, http):
    with open(file, 'r') as source:
        output = ''
        base = source.read()
        if http is True:
            base=base.replace('$#varnish-port#$','80')
        else:
            base=base.replace('$#varnish-port#$','90')
    with open(file, 'w') as result:
        result.write(base)
    return

def make_multiple_nifi(dashboard_ip, kafka_ip, main_opensearch_ip, ips, token, zookeper_ip):
    nodes_ips = ''
    components_ips = """      - dashboard:"""+dashboard_ip+"""
  - opensearch-n1:"""+main_opensearch_ip+"""
  - kafka:"""+kafka_ip
    # ports are hardcoded here and in flow, when active
    ports = [str(i) for i in range(1026, 1036)]
    i = 1
    for ip in ips:
        nodes_ips+='      - nifi-node-'+str(i)+':'+ip+'\n'
        i+=1
    j = 0
    while j < len(ips):
        os.makedirs('./Output/'+token+'/'+ips[j]+'/nifi/conf', exist_ok=True)
        for file in ['authorizers.xml','bootstrap-notification-services.xml','bootstrap.conf','enrich-data.conf','logback.xml','login-identity-providers.xml','state-management.xml','zookeeper.properties']:

            copy('./Modules/nifi/conf/'+file, './Output/'+token+'/'+ips[j]+'/nifi/conf/'+file)
        copy('./Modules/varnish', './Output/'+token+'/'+ips[j]+'/varnish')
        copy('./Modules/docker-compose-nifi-slave.yml', './Output/'+token+'/'+ips[j]+'/docker-compose-nifi-slave.yml')
        with open('./Output/'+token+'/'+ips[j]+'/docker-compose-nifi-slave.yml','r') as f:
            s=f.read()
        if j == 0:
            s=s.replace('$#extra_hosts#$',nodes_ips+'\n'+components_ips)
        else:
            s=s.replace('$#extra_hosts#$',nodes_ips)
        s=s.replace('$#id_ip#$',ips[j])
        s=s.replace('$#node_name#$','nifi-node-'+str(j+1))
        s=s.replace('$#id_zookeeper#$',zookeper_ip)
        with open('./Output/'+token+'/'+ips[j]+'/docker-compose-nifi-slave.yml','w') as f:
            f.write(s)
        j+=1
    return

def make_multiple_opensearch(how_many, dashboard_ip, ldap_ip, token, ips, alt_out=None):
    outdir = ''
    if alt_out is None:
        outdir = './Output/'+token+'/'+ips[i]
    else:
        outdir = alt_out
    all_ips, less_ips, seed_names, credentials = '','','',''
    i=0
    for ip in ips:
        less_ips+='      - opensearch-n'+str(i+1)+':'+ip+'\n'
        seed_names+='opensearch-n'+str(i+1)+','
        credentials+='  - "CN=opensearch-n'+str(i+1)+',O=SNAP4,L=Florence,ST=Toscana,C=IT"\n'
        i+=1
    seed_names=seed_names[:-1]
    all_ips='      - dashboard:'+dashboard_ip+'\n      - ldap-server:'+ldap_ip+'\n'+less_ips
    i=0
    while i < how_many:
        currentfolder = '/opensearch-conf-'+str(i)
        copy('./Modules/opensearch-conf', outdir+currentfolder)
        copy('./Modules/opensearch-conf+/opensearch.yml',outdir+currentfolder+'/opensearch.yml')
        if i == 0:
            copy('./Modules/docker-compose-elastic-multi-master.yml', outdir+'/docker-compose-elastic-multi-master.yml')
            copy('./Modules/opensearch-conf+/gen_certs_master.sh',outdir+currentfolder+'/gen-certs.sh')
        else:
            copy('./Modules/docker-compose-elastic-multi-slave.yml', outdir+'/docker-compose-elastic-multi-slave-'+str(i)+'.yml')
            copy('./Modules/opensearch-conf+/gen_certs.sh',outdir+currentfolder+'/gen-certs.sh')

        with open(outdir+currentfolder+'/gen-certs.sh', 'r') as f:
            q=f.read()
            q=q.replace('$#node_name#$','opensearch-n'+str(i+1))
        with open(outdir+currentfolder+'/gen-certs.sh','w') as f:
            f.write(q)
        if i == 0:
            with open(outdir+'/docker-compose-elastic-multi-master.yml','r') as f:
                s=f.read()
        else:
            with open(outdir+'/docker-compose-elastic-multi-slave-'+str(i)+'.yml','r') as f:
                s=f.read()
        s=s.replace('$#hosts_less#$',less_ips)
        s=s.replace('$#extra_hosts#$',all_ips)
        s=s.replace('$#id_ip#$',ips[i])
        s=s.replace('$#node_name#$','opensearch-n'+str(i+1))
        s=s.replace('$#seed_hosts#$',seed_names)
        if i == 0:
            with open(outdir+'/docker-compose-elastic-multi-master.yml','w') as f:
                f.write(s)
        else:
            with open(outdir+'/docker-compose-elastic-multi-slave-'+str(i)+'.yml','w') as f:
                f.write(s)
        with open(outdir+currentfolder+'/opensearch.yml','r') as f:
            s=f.read()
        s=s.replace('$#credentials#$',credentials)
        with open(outdir+currentfolder+'/opensearch.yml','w') as f:
            f.write(s)

        i+=1

def add_tests(destination_path):
    copy('./auto_tests', destination_path)

def placeholders_in_folder(placeholders, path_of_folder):
    for dname, dirs, files in os.walk(path_of_folder):
        for file in files:
            placeholders_in_file(os.path.join(dname,file),placeholders)


def add_utils(destination_path):
    copy('./utilsAndTools', destination_path)
    
def copy(source, dest):
    """Tries to copy a file from source to destination; if it's not file, try to copy as a folder, fail otherwise"""
    try:
        shutil.copy(source, dest)
    except IsADirectoryError:
        try:
            shutil.copytree(source, dest)
        except Exception as E:
            raise E
    return

#TODO "end of files" volumes are not generated and they should be
def docker_to_kubernetes(location, hostname, namespace, final_path='/mnt/data/generated'):
    # unfortunately, docker-compose config was edited in a such way it broke some usages, even if the devs say that's intended
    # nevermind that they deleted tests that were failing on that release
    # therefore yq is used to fix the mistake, which happens on the depends_on attribute
    # however THAT also gives problem, because it will give a depends_on where there is no such thing
    # we can complete the preconfig with sed, removing the wrong lines
    if not os.path.exists(location):
        print("[LOG] The location provided wasn't valid (",location,"), won't proceed with kubernetes convertion.")
    #
    os.system('''cd ''' + location + '''
    mkdir kubernetes
    cp docker-compose.yml kubernetes/docker-compose.yml
    cd kubernetes
    docker-compose config | yq e '(.services[] | select(.depends_on | tag == "!!map")).depends_on |= (. | keys)' - > file.yml
    rm docker-compose.yml
    cp file.yml docker-compose.yml
    rm file.yml
    sed -i '/depends_on: null/d' ./docker-compose.yml''')

    with open(location+'/kubernetes/docker-compose.yml', 'r') as f:
        test_str = f.read()

    # remove problematic volumes
    regex = r"\s *(\w*)- ([\w-])+.*\w:rw"

    subst = ""

    #result = re.sub(regex, subst, test_str, 0, re.MULTILINE)
    result = test_str
    # remove the volume section if it is empty
    regex2 = r" +volumes:(\s*\w)"

    subst2 = "\\1"

    result = re.sub(regex2, subst2, result, 0, re.MULTILINE)
    # force the ports to be the same in and out
    regex3 = r"( *- published: )(\d{2,5})(\s*target: )(?!\2)(\d{2,5})"

    subst3 = "\\1\\2\\3\\2"

    result = re.sub(regex3, subst3, result, 0, re.MULTILINE)

    #make all iot-apps port 1880
    regex4 = r"(iotapp[\w\s\d\-_\/.' :]*?)([1][8-9][0-9][0-9])([\w\s\d\-_\/.' :]*?)([1][8-9][0-9][0-9])([\w\s\d\-_\/.' :]*?iotapp)"

    subst4 = "\\1 1880 \\3 1880 \\5"

    result = re.sub(regex4, subst4, result, 0, re.MULTILINE)

    # for each service, add a label to add tell kompose to expose the service
    # make the services as nodeports
    #            a|b
    regex5 = r"^(  )([\w-]+)(:)$"

    subst5 = '\\1\\2\\3\n\\1\\1labels:\n\\1\\1\\1kompose.service.expose: "true"\n\\1\\1\\1kompose.service.type: "nodeport"\n\\1\\1\\1kompose.volume.storage-class-name: "efs-sc"' #kompose.volume.storage-class-name

    result = re.sub(regex5, subst5, result, 0, re.MULTILINE)

    #adjustments

    # servicemap port needs to be set to 8080
    result=result.replace("8090","8080")
    # builder needs the port to be set to 80
    result=result.replace(" 70"," 80")
    # wsserver needs the port to be fixed
    result=result.replace("9100","8000")
    with open(location+'/kubernetes/docker-compose.yml', 'w') as f:
        f.write(result)


    # finally we are ready for kompose, using hostPath for volumes
    # but paths become absolute; we'll fix them on the deployed machine
    # then update the name of the proxy
    os.system('''cd ''' + location + '''/kubernetes
    kompose convert --volumes persistentVolumeClaim
    sed -i 's@name: proxy@name: '''+hostname+'''@' ./proxy-service.yaml''')

    for dname, dirs, files in os.walk(location+'/kubernetes'):
        for file in files:
            path = '/Flask'+location[1:]
            with open(os.path.join(dname,file), 'r') as f:
                data=f.read()
            data = re.sub(r'(name: )([a-zA-Z0-9-]*)([\w|\W]*)(path: '+path+')(/kubernetes)(\s)',r'\1\2\3\4/volumes/\2-volume\6',data)
            # /Flask/Output/d151c7ce869dbc472534b7286696cbf1bec2d9c9/192.168.1.18/kubernetes
            # /Flask/Output/d151c7ce869dbc472534b7286696cbf1bec2d9c9/192.168.1.18/kubernetes\/volumes\/kafka\-volume
            # /mnt/data/generated2.168.1.18/volumes/kafka-volume

            data = data.replace(path,final_path)
            with open(os.path.join(dname,file), 'w') as f:
                f.write(data)
    data_volumes = ""

    if True:
        with open(location+'/kubernetes/docker-compose.yml', 'r') as f:
            data_volumes = f.read()
        lines = data_volumes.split("\n")
        data_lines = [a for a in lines if "- /mnt" in a]
        data_lines = [a.strip() for a in data_lines]
        data_lines = [a[2:a.find(':')] for a in data_lines]
        for dname, dirs, files in os.walk(location+'/kubernetes'):
            for file,volume_path in zip(sorted([file for file in files if 'persistentvolumeclaim' in file]),data_lines):
                if 'persistentvolumeclaim' in file:
                    temporary = ''
                    vname=''
                    with open('./Modules/kubernetes/dummy-persistentVolume.yaml', 'r') as f:
                        temporary = f.read()
                        vname=file[file.rfind('\\')+1:file.rfind('-')]

                        temporary=temporary.replace('$#volume-name#$',vname)
                        temporary=temporary.replace('$#volume-path#$',volume_path.replace("/kubernetes",""))
                        #print(location+'/kubernetes/'+vname+'-persistentvolume.yaml')
                    with open(location+'/kubernetes/'+vname+'-persistentvolume.yaml', 'w') as f:
                        f.write(temporary)

    # WARNS to be solved
    # Service * won't be created if 'ports' is not specified
    #fixing cron

# (name: )([a-zA-Z0-9-]*)([\w|\W]*)(path: \/mnt\/data\/generated)(\s)
#
# \1\2\3\4\/volumes\/\2\-volume\5
#
