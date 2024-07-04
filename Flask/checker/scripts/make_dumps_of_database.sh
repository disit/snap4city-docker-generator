#!/bin/bash

#docker exec 62149183138_dashboarddb_1 mysqldump -uroot -p'aeHus1fkPIZhasTB' --all-databases > mysql_dump.sql  #aeHus1fkPIZhasTB  - this copies logs which are gonna be huge
docker exec mongo-001 mongodump --out /dump; docker cp mongo-001:/dump mongo_dump; docker exec mongo-001 rm -rf /dump
#todo what if multiple mongos?
docker exec $#virtuoso-pwd#$ mkdir -p /usr/local/virtuoso-opensource/share/virtuoso/vad/dump.nq; docker exec virtuoso-kb isql-v localhost dba $#virtuoso-pwd#$ exec="dump_nquads('/usr/local/virtuoso-opensource/share/virtuoso/vad/dump.nq')"; docker cp virtuoso-kb:/usr/local/virtuoso-opensource/share/virtuoso/vad/dump.nq virtuoso_dump.nq; docker exec virtuoso-kb rm -rf /usr/local/virtuoso-opensource/share/virtuoso/vad/dump.nq
docker exec od-postgis pg_dumpall -U postgres > postgres_od-postgis_dump.sql
docker exec postgres-db pg_dumpall -U keycloak > postgres_postgres-db_dump.sql
#todo postgres-s geoserver is cursed and doesn't like any user or password
