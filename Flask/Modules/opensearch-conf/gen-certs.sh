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
    -extfile <(printf "subjectAltName=IP:127.0.0.1,DNS:localhost,DNS:dashboard")'

# KEYSTORE / TRUSTSTORE
docker exec -e PASS="$TRUSTSTORE_PASSWD" nifi-setup bash -c 'keytool -import -file root-ca.pem -keystore nifi-node-truststore.jks \
    -deststoretype JKS -deststorepass "$PASS" -alias nifi-root-ca -noprompt'

docker exec -e PASS="$KEYSTORE_PASSWD" nifi-setup bash -c 'openssl pkcs12 -export -in nifi-node.pem -inkey nifi-node-key.pem \
    -name nifi-node -out nifi-node-keystore.pkcs12 -password pass:"$PASS"'
docker exec -e PASS="$KEYSTORE_PASSWD" nifi-setup bash -c 'keytool -importkeystore -srckeystore nifi-node-keystore.pkcs12 \
    -srcstoretype PKCS12 -destkeystore nifi-node-keystore.jks -deststoretype JKS \
    -srcstorepass "$PASS" -deststorepass "$PASS"'

# Substitute passwords in nifi.properties
sed -i \
    -e "s/^nifi.sensitive.props.key=.*/nifi.sensitive.props.key=${SENSITIVE_PROPS_KEY}/" \
    -e "s/^nifi.security.keystorePasswd=.*/nifi.security.keystorePasswd=${KEYSTORE_PASSWD}/" \
    -e "s/^nifi.security.keyPasswd=.*/nifi.security.keyPasswd=${KEYSTORE_PASSWD}/" \
    -e "s/^nifi.security.truststorePasswd=.*/nifi.security.truststorePasswd=${TRUSTSTORE_PASSWD}/" \
    ../nifi/conf/nifi.properties

# Copy certificates to host
mkdir certs
docker cp nifi-setup:/root-ca-key.pem ./certs/root-ca-key.pem
docker cp nifi-setup:/root-ca.pem ./certs/root-ca.pem

docker cp nifi-setup:/nifi-node-key.pem ./certs/nifi-node-key.pem
docker cp nifi-setup:/nifi-node.pem ./certs/nifi-node.pem

docker cp nifi-setup:/nifi-node-truststore.jks ./certs/nifi-node-truststore.jks
docker cp nifi-setup:/nifi-node-keystore.jks ./certs/nifi-node-keystore.jks

# TODO: copy the admin certificate to host

# Stop nifi-setup container and clean-up 
docker stop nifi-setup

## Copy certs to the conf folder
cp certs/nifi-node-truststore.jks ../nifi/conf/truststore.jks
cp certs/nifi-node-keystore.jks ../nifi/conf/keystore.jks

