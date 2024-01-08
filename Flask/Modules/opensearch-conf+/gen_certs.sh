#!/bin/sh
# Root CA
C=IT
ST=Toscana
L=Florence
O=SNAP4
OU=
CN=$#node_name#$

# Node cert
echo
echo generate node cert
openssl genrsa -out node-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in node-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node-key.pem
openssl req -new -key node-key.pem -subj "/C=$C/ST=$ST/L=$L/O=$O/OU=$OU/CN=$CN" -out node.csr
openssl x509 -req -in node.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node.pem -days 3650

chmod a+r *-key.pem

# Cleanup
rm node-key-temp.pem
rm node.csr

echo remember to copy the other certificates from the configuration of opensearch-n1
echo otherwise this will not work

sysctl -w vm.max_map_count=262144
