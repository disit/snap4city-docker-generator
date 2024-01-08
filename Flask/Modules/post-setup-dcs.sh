cd servicemap-$#id#$-conf
./update-ontology.sh localhost
docker-compose exec virtuoso-kb-$#id#$ isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap.vt
docker-compose exec virtuoso-kb-$#id#$ isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap-dbpedia.vt

cd ..
