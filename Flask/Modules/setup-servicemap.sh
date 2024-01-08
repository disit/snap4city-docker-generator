mkdir servicemap-conf/logs
mkdir servicemap-iot-conf/logs
mkdir servicemap-iot-conf/logs/insert
mkdir servicemap-iot-conf/logs/delete
mkdir servicemap-iot-conf/logs/list-static-attr
chmod a+w servicemap-conf/logs
chmod a+w servicemap-iot-conf/logs
chmod a+w servicemap-iot-conf/logs/insert
chmod a+w servicemap-iot-conf/logs/delete
chmod a+w servicemap-iot-conf/logs/list-static-attr
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144
