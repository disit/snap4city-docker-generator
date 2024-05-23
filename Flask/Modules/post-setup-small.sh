ANON=$(docker run --rm php:latest php -r '
    $key = hash("sha256", "$#aes-encryption-key-16chars#$");
    $iv = substr(hash("sha256", "$#aes-encryption-iv-16chars#$"), 0, 16);
    $output = openssl_encrypt("$#virtuoso-kb-pwd#$", "AES-256-CBC", $key, 0, $iv);
    $output = base64_encode($output);
    echo $output;
')
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


echo create opensearch ot-device-state index
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/ot-device-state' -d @mapping_DeviceState-ES7-v1.json
echo

echo setup role areamanager
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_areamanager' -d @- << EOF
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
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_areamanager' -d @- << EOF
{
  "backend_roles" : [ "AreaManager" ]
}
EOF
echo

echo setup role manager
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_manager' -d @- << EOF
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
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_manager' -d @- << EOF
{
  "backend_roles" : [ "Manager" ]
}
EOF
echo

echo setup role tooladmin
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_tooladmin' -d @- << EOF
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
curl --insecure -u admin:admin -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_tooladmin' -d @- << EOF
{
  "backend_roles" : [ "ToolAdmin" ]
}
EOF
echo

echo add dashboard
curl -u admin:admin -XPOST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "osd-xsrf: true" -H "securitytenant: global" --form file=@osd-dashboard.ndjson
echo

echo add geoserver workspace Snap4City
curl -u admin:$#postgre-geo-password#$ -XPOST -H "Content-type: text/xml" -d "<workspace><name>Snap4City</name></workspace>"  http://localhost/geoserver/rest/workspaces


echo rebooting service
docker-compose restart opensearch-dashboards personaldata iot-fiware-harvester
