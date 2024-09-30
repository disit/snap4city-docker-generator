# note: this is still experimental
kubectl -n $#k8-namespace#$ exec deployment/servicemap  --  bash -c "cd /root/servicemap; ./update-ontology-k8.sh virtuoso-kb"
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap.vt
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/valuetypes.vt
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap-dbpedia.vt


cd servicemap-conf


ANON=$(kubectl -n snap4city exec deployment/dashboard-builder -- php -r '$key = hash("sha256", "$#aes-encryption-key-16chars#$");
    $iv = substr(hash("sha256", "$#aes-encryption-iv-16chars#$"), 0, 16);
    $output = openssl_encrypt("$#virtuoso-kb-pwd#$", "AES-256-CBC", $key, 0, $iv);
    $output = base64_encode($output);
    echo $output;')
echo the new anonymous hash is $ANON

##curl -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/iotdata-organization' -d @mapping_Sensors-ETL-IOT-v3.json



echo create opensearch iot index
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/snap4-iot-organization' -d @mapping_Sensors-ETL-IOT-ES7-v4.json
echo

echo create opensearch kpi index
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/snap4-kpi' -d @mapping_Sensors-ETL-IOT-ES7-v4.json
echo


echo setup role areamanager
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_areamanager' -d @- << EOF
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
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_areamanager' -d @- << EOF
{
  "backend_roles" : [ "AreaManager" ]
}
EOF
echo

echo setup role manager
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_manager' -d @- << EOF
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
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_manager' -d @- << EOF
{
  "backend_roles" : [ "Manager" ]
}
EOF
echo

echo setup role tooladmin
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/roles/kibanauser_tooladmin' -d @- << EOF
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
kubectl -n snap4city exec deployment/servicemap  --  curl --insecure -u admin:$#opensearch-admin-pwd#$ -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/_plugins/_security/api/rolesmapping/kibanauser_tooladmin' -d @- << EOF
{
  "backend_roles" : [ "ToolAdmin" ]
}
EOF
echo

echo add dashboard
curl --insecure -u admin:$#opensearch-admin-pwd#$ -XPOST "$#base-url#$/kibana/api/saved_objects/_import?overwrite=true" -H "osd-xsrf: true" -H "securitytenant: global" --form file=@osd-dashboard.ndjson
echo

echo fixing openldap admin password
kubectl -n snap4k8s exec deployment/ldap-server -- bash /ldif_files/psw.sh

cd ..
echo "fixing keycloak (for this to work, the system must be able to recognize its own hostname)"
python3 keycloak-conf/keycloak-rest.py $#base-url#$/auth admin $#keycloak-admin-pwd#$
python3 keycloak-conf/keycloak-step-2.py
echo running again to fix first execution
python3 keycloak-conf/keycloak-step-2.py
