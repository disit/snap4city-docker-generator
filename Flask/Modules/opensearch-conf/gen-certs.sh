#!/bin/bash

cd "$(dirname "$0")"

# Start the setup container
docker run --rm --name nifi-setup -d eclipse-temurin:21 tail -f /dev/null

# Generate passwords   # using placeholders generated elsewhere
SENSITIVE_PROPS_KEY=$#nifi-enc-key#$
KEYSTORE_PASSWD=$#keystore-password#$
TRUSTSTORE_PASSWD=$#truststore-password#$
SINGLE_USER_PASSWD=$#nifi-password#$

echo "Sensitive props key = ${SENSITIVE_PROPS_KEY}"
echo "Keystore password = ${KEYSTORE_PASSWD}"
echo "Truststore password = ${TRUSTSTORE_PASSWD}"

# Generate certificates
# ROOT CA
docker exec nifi-setup openssl genrsa -out root-ca-key.pem 2048
docker exec nifi-setup openssl req -new -x509 -sha256 -key root-ca-key.pem \
    -subj "/C=CC/ST=State/L=Location/O=Organiztion/OU=org-unit/CN=nifi-root-ca" \
    -days 18250 -out root-ca.pem

# NODE CERTIFICATE
docker exec nifi-setup openssl genrsa -out nifi-node-key-temp.pem 2048
docker exec nifi-setup openssl pkcs8 -inform PEM -in nifi-node-key-temp.pem \
    -topk8 -nocrypt -v1 PBE-SHA1-3DES -out nifi-node-key.pem

docker exec nifi-setup openssl req -new -key nifi-node-key.pem \
    -subj "/C=CC/ST=State/L=Location/O=Organiztion/OU=org-unit/CN=nifi-node" \
    -out nifi-node.csr

docker exec nifi-setup bash -c 'openssl x509 -req -in nifi-node.csr \
    -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -days 18250 \
    -out nifi-node.pem \
    -extfile <(printf "subjectAltName=IP:127.0.0.1,DNS:localhost,DNS:dashboard,DNS:opensearch-n1")'

# KEYSTORE / TRUSTSTORE
docker exec -e PASS="$TRUSTSTORE_PASSWD" nifi-setup bash -c 'keytool -import -file root-ca.pem -keystore nifi-node-truststore.jks \
    -deststoretype JKS -deststorepass "$PASS" -alias nifi-root-ca -noprompt'

docker exec -e PASS="$KEYSTORE_PASSWD" nifi-setup bash -c 'openssl pkcs12 -export -in nifi-node.pem -inkey nifi-node-key.pem \
    -name nifi-node -out nifi-node-keystore.pkcs12 -password pass:"$PASS"'
docker exec -e PASS="$KEYSTORE_PASSWD" nifi-setup bash -c 'keytool -importkeystore -srckeystore nifi-node-keystore.pkcs12 \
    -srcstoretype PKCS12 -destkeystore nifi-node-keystore.jks -deststoretype JKS \
    -srcstorepass "$PASS" -deststorepass "$PASS"'

mkdir certs

docker cp nifi-setup:/root-ca-key.pem ./certs/root-ca-key.pem   # maybe useless?
docker cp nifi-setup:/root-ca.pem ./certs/root-ca.pem           # maybe useless?

docker cp nifi-setup:/nifi-node-key.pem ./certs/nifi-node-key.pem
docker cp nifi-setup:/nifi-node.pem ./certs/nifi-node.pem

docker cp nifi-setup:/nifi-node-truststore.jks ./certs/nifi-node-truststore.jks
docker cp nifi-setup:/nifi-node-keystore.jks ./certs/nifi-node-keystore.jks

# TODO: copy the admin certificate to host

# Stop nifi-setup container and clean-up 
docker stop nifi-setup

chown -R 1000:1000 certs/*.*

docker run --rm --name nifi-setup -d apache/nifi:2.2.0

docker exec -ti nifi-setup bash /opt/nifi/scripts/start.sh  # this will make the files in the temporary container

cp ../nifi/conf/flow.json.gz flow.json.gz # copy the og flow someplacelse

rm -r ../nifi/conf  # delete old folder because, for some reason, it doesn't work

docker cp nifi-setup:/opt/nifi/nifi-current/conf/ ../nifi

cp -f flow.json.gz ../nifi/conf/flow.json.gz # paste it after the new files are there

## Copy certs to the conf folders
cp certs/nifi-node-truststore.jks ../nifi/conf/truststore.jks
cp certs/nifi-node-truststore.jks ../servicenap-conf/truststore.jks
cp certs/nifi-node-keystore.jks ../nifi/conf/keystore.jks


sed -i \
    -e "s/^nifi.web.proxy.host=.*/nifi.web.proxy.host=$#base-hostname#$, localhost, $#base-hostname#$:9090/" \
    -e "s/^nifi.web.https.host=.*/nifi.web.https.host=0.0.0.0/" \
    -e "s/^nifi.remote.input.host=.*/nifi.remote.input.host=0.0.0.0/" \
    -e "s/^nifi.sensitive.props.key=.*/nifi.sensitive.props.key=$#nifi-enc-key#$/" \
    -e "s/^nifi.security.keystoreType=.*/nifi.security.keystoreType=JKS/" \
    -e "s/^nifi.security.truststoreType=.*/nifi.security.truststoreType=JKS/" \
    -e "s@^nifi.security.keystore=.*@nifi.security.keystore=./conf/keystore.jks@" \
    -e "s@^nifi.security.truststore=.*@nifi.security.truststore=./conf/truststore.jks@" \
    -e "s/^nifi.security.keystorePasswd=.*/nifi.security.keystorePasswd=$#keystore-password#$/" \
    -e "s/^nifi.security.keyPasswd=.*/nifi.security.keyPasswd=$#keystore-password#$/" \
    -e "s/^nifi.security.truststorePasswd=.*/nifi.security.truststorePasswd=$#truststore-password#$/" \
    ../nifi/conf/nifi.properties

chown 1000:1000 ../nifi/conf/*.*
chown 1000:1000 ../nifi/conf
chown 1000:1000 ../nifi/logs

docker stop nifi-setup
#docker compose exec nifi ./bin/nifi.sh set-single-user-credentials admin V5SFXfCsIPKAu4NN

