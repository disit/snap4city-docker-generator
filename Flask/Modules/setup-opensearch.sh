echo fixing opensearch internal users

hashadmin=$(docker run opensearchproject/opensearch:1.2.3 plugins/opensearch-security/tools/hash.sh -p $#opensearch-admin-pwd#$)
hashuser=$(docker run opensearchproject/opensearch:1.2.3 plugins/opensearch-security/tools/hash.sh -p $#kibanauser-password#$)

echo the new hash for the admin password is $hashadmin
echo the new hash for the user password is $hashuser

#create the file which will be used
cd opensearch-conf
cp internal_users.yml.tpl internal_users.yml

# we are replacing old hashes, and we need to escape some characters while using sed
sed -i "s|admin_replacing|$hashadmin|" "internal_users.yml"
sed -i "s|kibanaserver_replacing|$hashuser|" "internal_users.yml"
