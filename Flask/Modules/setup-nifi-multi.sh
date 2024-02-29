#!/bin/bash
chmod a+w nifi/conf
chmod a+w nifi/conf/flow.xml.gz
chmod a+w nifi/extensions
chmod u+x opensearch-conf/gen-certs.sh
mkdir -p datamanager-conf
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144

# new for elastic -> search
cd opensearch-conf
./gen-certs.sh

#set up certificates nifi
cd ..
docker-compose up -d nifi
docker run --rm --name toolkit -d apache/nifi:1.16.2
docker exec -ti toolkit /opt/nifi/nifi-toolkit-current/bin/tls-toolkit.sh standalone -n 'localhost' -C 'CN=admin, OU=NIFI' --subjectAlternativeNames '$#nifi-ips#$,0.0.0.0d' -S $#keystore-password#$ -P $#truststore-password#$

docker cp toolkit:/opt/nifi/nifi-current/nifi-cert.pem nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/nifi-key.key nifi/conf/

docker cp toolkit:/opt/nifi/nifi-current/localhost/truststore.jks  nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/localhost/nifi.properties  nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/localhost/keystore.jks  nifi/conf/

docker cp toolkit:/opt/nifi/nifi-current/CN=admin_OU=NIFI.p12      nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/CN=admin_OU=NIFI.password nifi/conf/
docker stop toolkit > /dev/null 2>&1

docker-compose exec nifi ./bin/nifi.sh set-single-user-credentials $#nifi-user#$ $#nifi-password#$
echo "new credentials for nifi should have been applied now if no error was shown"
docker-compose down
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
