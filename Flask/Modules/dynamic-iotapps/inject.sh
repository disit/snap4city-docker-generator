#!/bin/bash

echo "this script will add 2 containers to the (copy of) docker-compose.yml file, then allows the dashboard-builder to see and comminicate with those 2 containers"
echo
echo "besides that, it also restores the dynamic creation and status acquiring of new iotapps, implemented in docker"

docker cp createIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/createIotApplication.php
docker cp deleteIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/deleteIotApplication.php
docker cp statusIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/statusIotApplication.php
docker cp index.php dashboard-builder:/var/www/html/snap4city-application-api/v1/index.php

python3 -c 'import os, yaml;
additional_yaml=None
with open("dynamic-iotapps/docker-compose.yml", "r") as f1:
    additional_yaml = yaml.load(f1, Loader=yaml.FullLoader); 

with open("docker-compose.yml", "r") as f2: 
    loaded_yaml = yaml.load(f2, Loader=yaml.FullLoader);
    for container_name, container_data in additional_yaml['services'].items():
        loaded_yaml['services'][container_name]=container_data
    for container_name, container_data in loaded_yaml["services"].items(): 
        container_data["networks"] = ["default"]; 
    try: 
        loaded_yaml["services"]["dashboard-builder"]["networks"] = ["default", "protected"]; 
        loaded_yaml["networks"] = {"default": {"driver": "bridge"}, "protected": {"driver": "bridge"}}; 
    except Exception as E: 
        print("something failed:" + str(E)); 
    with open(file[:-4] + "-edited.yml", "w") as f2: 
        yaml.dump(loaded_yaml, f2)' 
