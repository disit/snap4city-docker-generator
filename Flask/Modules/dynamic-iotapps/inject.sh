#!/bin/bash

echo "this script will add 2 containers to the (copy of) docker-compose.yml file, then allows the dashboard-builder to see and comminicate with those 2 containers"
echo
echo "besides that, it also restores the dynamic creation and status acquiring of new iotapps, implemented in docker"

docker cp createIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/createIotApplication.php
docker cp deleteIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/deleteIotApplication.php
docker cp statusIotApplication.php dashboard-builder:/var/www/html/dashboardSmartCity/controllers/statusIotApplication.php
docker cp index.php dashboard-builder:/var/www/html/snap4city-application-api/v1/index.php

python3 inject.py
