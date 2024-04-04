cd servicemap-conf
source ./update-ontology.sh localhost
x_exit_code=$?

if [ $x_exit_code -ne 0 ]; then
    echo "Sourcing ontologies failed, trying second method..."
    
    ./update-ontology.sh localhost
    y_exit_code=$?

    if [ $y_exit_code -eq 0 ]; then
        echo "The second method worked, continuing..."
        
    else
        echo "Can't proceed"
		exit -1
    fi
fi
docker-compose exec virtuoso-kb isql-v localhost dba $#virtuoso-kb-pwd#$ /root/servicemap/servicemap.vt
docker-compose exec virtuoso-kb isql-v localhost dba $#virtuoso-kb-pwd#$ /root/servicemap/valuetypes.vt
docker-compose exec virtuoso-kb isql-v localhost dba $#virtuoso-kb-pwd#$ /root/servicemap/servicemap-dbpedia.vt