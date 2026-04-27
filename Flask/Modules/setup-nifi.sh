mkdir -p varnish/logs
mkdir -p nifi/logs
chmod a+w nifi/conf -R
chmod a+w nifi/conf/flow.json.gz
chmod a+w nifi/logs
chmod 777 varnish/docker-entrypoint
chmod u+x opensearch-conf/gen-certs.sh
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144

# new for elastic -> search
cd opensearch-conf
./gen-certs.sh

#set up certificates nifi
cd ..
#!/bin/bash
docker compose up -d nifi

docker compose exec nifi ./bin/nifi.sh set-single-user-credentials $#nifi-user#$ $#nifi-password#$
echo "new credentials for nifi should have been applied now if no error was shown"
docker compose down
file="nifi/conf/nifi.properties"
#parsing the file
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value} > /dev/null 2>&1
done < "$file"

echo "Truststore password = " ${nifi_security_truststorePasswd}
echo "Keystore password =   " ${nifi_security_keystorePasswd}

sed -i "s|ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB|$#nifi-password#$|" "docker-compose.yml"
sed -i "s|keystorepassword_replace_me|${nifi_security_keystorePasswd}|" "docker-compose.yml"
sed -i "s|truststorepassword_replace_me|${nifi_security_truststorePasswd}|" "docker-compose.yml"

echo "updated nifi in compose file"
echo "fixing chmod perms for generated nifi files"
sudo chmod 644 nifi/conf/*
