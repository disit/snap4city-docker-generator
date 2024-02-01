#!/bin/bash
#set -e

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
#new addition
docker-compose exec virtuoso-kb /bin/bash -c "sync && /usr/local/virtuoso-opensource/bin/isql-v 1111 -U dba -P $#virtuoso-kb-pwd#$ 'EXEC=checkpoint;'"
##note: split this for opensearch
##curl -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/iotdata-organization' -d @mapping_Sensors-ETL-IOT-v3.json

echo create opensearch iot index
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/snap4-iot-organization' -d @mapping_Sensors-ETL-IOT-ES7-v4.json
echo

echo create opensearch iot-device-state index
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/iot-device-state' -d @mapping_DeviceState-ES7-v1.json
echo

echo create opensearch kpi index
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/snap4-kpi' -d @mapping_Sensors-ETL-IOT-ES7-v4.json
echo

echo setup role areamanager
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_areamanager' -d @- << EOF
{
  "cluster_permissions": [
    "*"
  ],
  "index_permissions": [{
    "index_patterns": [
      "snap4-*"
    ],
    "dls": "{\"bool\":{\"should\":[{\"match\":{\"username\": \"\${attr.jwt.uid}\"}},{\"match\": {\"user_delegations\": \"\${attr.jwt.uid}\"}},{\"bool\":{\"must\":[{\"match\":{\"user_delegations\": \"$ANON\"}},{\"match\": {\"organization\": \"\${attr.jwt.ou}\"}}]}},{\"match\": {\"organization_delegations\": \"\${attr.jwt.ou}\"}}],\"minimum_should_match\": 1}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
EOF
echo

echo setup rolemapping areamanager
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_areamanager' -d @- << EOF
{
  "backend_roles" : [ "AreaManager" ]
}
EOF
echo

echo setup role manager
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_manager' -d @- << EOF
{
  "cluster_permissions": [
    "*"
  ],
  "index_permissions": [{
    "index_patterns": [
      "snap4-*"
    ],
    "dls": "{\"bool\":{\"should\":[{\"match\":{\"username\": \"\${attr.jwt.uid}\"}},{\"match\": {\"user_delegations\": \"\${attr.jwt.uid}\"}},{\"bool\":{\"must\":[{\"match\":{\"user_delegations\": \"$ANON\"}},{\"match\": {\"organization\": \"\${attr.jwt.ou}\"}}]}},{\"match\": {\"organization_delegations\": \"\${attr.jwt.ou}\"}}],\"minimum_should_match\": 1}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
EOF
echo

echo setup rolemapping manager
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_manager' -d @- << EOF
{
  "backend_roles" : [ "Manager" ]
}
EOF
echo

echo setup role tooladmin
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_tooladmin' -d @- << EOF
{
  "cluster_permissions": [
    "*"
  ],
  "index_permissions": [{
    "index_patterns": [
      "snap4-*"
    ],
    "dls": "{\"bool\":{\"should\":[{\"match\":{\"organization\":\"\${attr.jwt.ou}\"}},{\"match\":{\"user_delegations\":\"\${attr.jwt.uid}\"}},{\"match\":{\"user_delegations\":\"$ANON\"}},{\"match\":{\"organization_delegations\":\"\${attr.jwt.ou}\"}}],\"minimum_should_match\":1}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
EOF
echo

echo setup rolemapping tooladmin
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_tooladmin' -d @- << EOF
{
  "backend_roles" : [ "ToolAdmin" ]
}
EOF
echo

echo add dashboard
curl --insecure -u admin:$#opensearch-admin-pwd#$ -XPOST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "osd-xsrf: true" -H "securitytenant: global" --form file=@osd-dashboard.ndjson
echo

echo add geoserver workspace Snap4City
curl -u admin:$#postgre-geo-password#$ -XPOST -H "Content-type: text/xml" -d "<workspace><name>Snap4City</name></workspace>"  http://localhost/geoserver/rest/workspaces


echo rebooting services
docker-compose restart opensearch-dashboards wsserver iot-fiware-harvester varnish proxy
echo fixing openldap admin password
docker-compose exec ldap-server bash /ldif_files/psw.sh
