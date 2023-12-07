chmod a+w orionbrokerfilter-*-logs

chmod -R a+w iotapp-*
chmod u+x opensearch-conf/gen-certs.sh
chmod a+w iot-directory-certificate
mkdir -p iot-directory-log
chmod a+w iot-directory-log
mkdir -p datamanager-conf
chmod a+wr datamanager-conf
mkdir servicemap-conf/logs
mkdir servicemap-iot-conf/logs
mkdir servicemap-iot-conf/logs/insert
mkdir servicemap-iot-conf/logs/delete
mkdir servicemap-iot-conf/logs/list-static-attr
mkdir servicemap-iot-conf/logs/move
chmod a+w servicemap-conf/logs
chmod a+w servicemap-iot-conf/logs
chmod a+w servicemap-iot-conf/logs/insert
chmod a+w servicemap-iot-conf/logs/delete
chmod a+w servicemap-iot-conf/logs/list-static-attr
chmod a+w servicemap-iot-conf/logs/move/
chmod a+w nifi/conf -R
chmod a+w nifi/conf/flow.xml.gz
chmod a+w nifi/extensions
mkdir -p nifi/logs
chmod 777 varnish/docker-entrypoint
mkdir -p ownership-conf/logs
mkdir -p datamanager-logs
chmod a+w ownership-conf/logs
chmod a+w datamanager-logs
mkdir -p certbot/logs
mkdir -p certbot/conf
mkdir -p certbot/work
mkdir -p certbot/www/.well-known/acme-challenge
chmod a+w certbot/www
chown -R 1000:1000 certbot
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144
chmod a+w orionbrokerfilter-*-logs
cd opensearch-conf
./gen-certs.sh

#set up certificates nifi
cd ..
#!/bin/bash
docker-compose up -d nifi
docker run --rm --name toolkit -d apache/nifi:1.16.2
docker exec -ti toolkit /opt/nifi/nifi-toolkit-current/bin/tls-toolkit.sh standalone -n 'localhost' -C 'CN=admin, OU=NIFI' -S SwmDiWo1woIbErlr -P Wx703cC1Vyb8ipAr

docker cp toolkit:/opt/nifi/nifi-current/nifi-cert.pem nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/nifi-key.key nifi/conf/

docker cp toolkit:/opt/nifi/nifi-current/localhost/truststore.jks  nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/localhost/nifi.properties  nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/localhost/keystore.jks  nifi/conf/

docker cp toolkit:/opt/nifi/nifi-current/CN=admin_OU=NIFI.p12      nifi/conf/
docker cp toolkit:/opt/nifi/nifi-current/CN=admin_OU=NIFI.password nifi/conf/
docker stop toolkit

docker-compose exec nifi ./bin/nifi.sh set-single-user-credentials admin evu17GUFxl50f6Jw
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

sed -i "s|ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB|evu17GUFxl50f6Jw|" "docker-compose.yml"
sed -i "s|keystorepassword_replace_me|${nifi_security_keystorePasswd}|" "docker-compose.yml"
sed -i "s|truststorepassword_replace_me|${nifi_security_truststorePasswd}|" "docker-compose.yml"

echo "updated nifi in compose file"
echo "fixing chmod perms for generated nifi files"
sudo chmod a+rw nifi/conf/*
echo fixing opensearch internal users

hashadmin=$(docker run opensearchproject/opensearch:1.2.3 plugins/opensearch-security/tools/hash.sh -p O2Ur2ey1afMpO1Tx)
hashuser=$(docker run opensearchproject/opensearch:1.2.3 plugins/opensearch-security/tools/hash.sh -p 1Ajfq6YcM2uSdTWL)

echo the new hash for the admin password is $hashadmin
echo the new hash for the user password is $hashuser

#create the file which will be used
cd opensearch-conf
cp internal_users.yml.tpl internal_users.yml

# we are replacing old hashes, and we need to escape some characters while using sed
sed -i "s|admin_replacing|$hashadmin|" "internal_users.yml"
sed -i "s|kibanaserver_replacing|$hashuser|" "internal_users.yml"
