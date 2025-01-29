#!/bin/bash

docker cp createIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/createIotApplication.php
docker cp deleteIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/deleteIotApplication.php
docker cp statusIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/statusIotApplication.php
docker cp index.php dashboard-builder:/var/www/html/snap4city-application-api/v1/index.php

python3 -c 'import os, yaml; 
for dname, _, files in os.walk("."): 
    for file in files: 
        if file.endswith(".yml"): 
            with open(file, "r") as f: 
                yyy = yaml.load(f, Loader=yaml.FullLoader); 
                for container_name, container_data in yyy["services"].items(): 
                    container_data["networks"] = ["default"]; 
                try: 
                    yyy["services"]["dashboard-builder"]["networks"] = ["default", "protected"]; 
                    yyy["networks"] = {"default": {"driver": "bridge"}, "protected": {"driver": "bridge"}}; 
                except Exception as E: 
                    print("something failed:" + str(E)); 
                with open(file[:-4] + "-edited.yml", "w") as f2: 
                    yaml.dump(yyy, f2)' 
