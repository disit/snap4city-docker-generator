#!/bin/sh

# note: this is still experimental

source update-ontology.sh localhost
kubectl -n snap4k8s exec deployment/servicemap  -- bash -c "cd /root/servicemap; ./update-ontology.sh virtuoso-kb"
kubectl -n snap4k8s exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
kubectl -n snap4k8s exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap.vt
kubectl -n snap4k8s exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/valuetypes.vt
kubectl -n snap4k8s exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap-dbpedia.vt

##curl -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/iotdata-organization' -d @mapping_Sensors-ETL-IOT-v3.json



echo create opensearch iot index
curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/snap4-iot-organization' -d @mapping_Sensors-ETL-IOT-ES7-v4.json
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
curl --insecure -u admin:$#opensearch-admin-pwd#$ -XPOST "http://localhost/kibana/api/saved_objects/_import?overwrite=true" -H "osd-xsrf: true" -H "securitytenant: global" --form file=@osd-dashboard.ndjson
echo

echo fixing openldap admin password
kubectl -n snap4k8s exec deployment/ldap-server -- bash /ldif_files/psw.sh