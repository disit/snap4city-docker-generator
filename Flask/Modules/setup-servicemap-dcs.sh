mkdir servicemap-$#id#$-conf/logs
mkdir servicemap-$#id#$-iot-conf/logs
mkdir servicemap-$#id#$-iot-conf/logs/insert
mkdir servicemap-$#id#$-iot-conf/logs/delete
mkdir servicemap-$#id#$-iot-conf/logs/list-static-attr
chmod a+w servicemap-$#id#$-conf/logs
chmod a+w servicemap-$#id#$-iot-conf/logs
chmod a+w servicemap-$#id#$-iot-conf/logs/insert
chmod a+w servicemap-$#id#$-iot-conf/logs/delete
chmod a+w servicemap-$#id#$-iot-conf/logs/list-static-attr
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144
