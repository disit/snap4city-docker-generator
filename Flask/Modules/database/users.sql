

-- CREATE USER '$#dashboard-db-user#$'@'%' IDENTIFIED BY '$#dashboard-db-pwd#$';  --this use is created on container boot
GRANT SELECT, INSERT, UPDATE ON Dashboard.* TO '$#dashboard-db-user#$'@'%';
GRANT SELECT, INSERT, UPDATE ON filemanagerdb.* TO '$#dashboard-db-user#$'@'%';
GRANT SELECT, INSERT, UPDATE ON datatable.* TO '$#dashboard-db-user#$'@'%';
GRANT SELECT, INSERT, UPDATE ON processloader_db.* TO '$#dashboard-db-user#$'@'%';

CREATE USER '$#heatmap-db-user#$'@'%' IDENTIFIED BY '$#heatmap-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON heatmap.* TO '$#heatmap-db-user#$'@'%';

CREATE USER '$#iotdirectory-db-user#$'@'%' IDENTIFIED BY '$#iotdirectory-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON iotdb.* TO '$#iotdirectory-db-user#$'@'%';

CREATE USER '$#notificator-db-user#$'@'%' IDENTIFIED BY '$#notificator-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON Notificator.* TO '$#notificator-db-user#$'@'%';

CREATE USER '$#servicemap-db-user#$'@'%' IDENTIFIED BY '$#servicemap-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON ServiceMap.* TO '$#servicemap-db-user#$'@'%';

CREATE USER '$#superservicemap-db-user#$'@'%' IDENTIFIED BY '$#superservicemap-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON SuperServiceMap.* TO '$#superservicemap-db-user#$'@'%';

CREATE USER '$#datamanager-db-user#$'@'%' IDENTIFIED BY '$#datamanager-db-pwd#$';
GRANT SELECT, INSERT, UPDATE ON profiledb.* TO '$#datamanager-db-user#$'@'%';