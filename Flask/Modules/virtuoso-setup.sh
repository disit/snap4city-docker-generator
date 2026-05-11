docker compose exec virtuoso-new isql localhost:1111 dba $#virtuoso-kb-pwd#$ /root/servicemap/servicemap.vt
docker compose exec virtuoso-new isql localhost:1111 dba $#virtuoso-kb-pwd#$ /root/servicemap/valuetypes.vt
docker compose exec virtuoso-new isql localhost:1111 dba $#virtuoso-kb-pwd#$ /root/servicemap/servicemap-dbpedia.vt
docker compose exec virtuoso-new /bin/bash -c "sync && isql localhost:1111 dba $#virtuoso-kb-pwd#$ 'EXEC=checkpoint;'"
