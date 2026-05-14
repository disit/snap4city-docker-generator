

-- CREATE USER '$#dashboard-db-user#$'@'%' IDENTIFIED BY '$#dashboard-db-pwd#$';  --this user is created on container boot
GRANT ALL ON Dashboard.* TO '$#dashboard-db-user#$'@'%';
GRANT ALL ON filemanagerdb.* TO '$#dashboard-db-user#$'@'%';
GRANT ALL ON datatable.* TO '$#dashboard-db-user#$'@'%';
GRANT ALL ON processloader_db.* TO '$#dashboard-db-user#$'@'%';
GRANT ALL ON iotdb.* TO '$#dashboard-db-user#$'@'%';
GRANT ALL ON profiledb.* TO '$#dashboard-db-user#$'@'%';

CREATE USER '$#heatmap-db-user#$'@'%' IDENTIFIED BY '$#heatmap-db-pwd#$';
GRANT ALL ON heatmap.* TO '$#heatmap-db-user#$'@'%';

CREATE USER '$#iotdirectory-db-user#$'@'%' IDENTIFIED BY '$#iotdirectory-db-pwd#$';
GRANT ALL ON iotdb.* TO '$#iotdirectory-db-user#$'@'%';

CREATE USER '$#notificator-db-user#$'@'%' IDENTIFIED BY '$#notificator-db-pwd#$';
GRANT ALL ON Notificator.* TO '$#notificator-db-user#$'@'%';

CREATE USER '$#servicemap-db-user#$'@'%' IDENTIFIED BY '$#servicemap-db-pwd#$';
GRANT ALL ON ServiceMap.* TO '$#servicemap-db-user#$'@'%';

CREATE USER '$#superservicemap-db-user#$'@'%' IDENTIFIED BY '$#superservicemap-db-pwd#$';
GRANT ALL ON SuperServiceMap.* TO '$#superservicemap-db-user#$'@'%';

CREATE USER '$#datamanager-db-user#$'@'%' IDENTIFIED BY '$#datamanager-db-pwd#$';
GRANT ALL ON profiledb.* TO '$#datamanager-db-user#$'@'%';