#!/bin/bash
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
echo "remember to chown the geoserver data also after the setup"
chown -R 1000 geoserver-data
#chmod a+w ckan-conf
sysctl -w vm.max_map_count=262144


read -p "try to use jdk8 for jdk? " choice

case "$choice" in
  y|Y|yes ) JDK8_HOME="$HOME/jdk8"
            CURRENT_JAVA_HOME=$(readlink -f $(which java) | sed "s:/bin/java::")
            ORIGINAL_PATH="$PATH"

            # # Check if JDK 8 is installed
            if [ ! -d "$JDK8_HOME" ]; then
              echo "JDK 8 is not installed. Downloading and installing JDK 8..."

              # Download and extract JDK 8 (using AdoptOpenJDK as an example)
              mkdir -p "$JDK8_HOME"
              curl -L -o jdk8.tar.gz https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u422-b05/openlogic-openjdk-8u422-b05-linux-x64.tar.gz

              # Extract the tarball
              tar -xzf jdk8.tar.gz --strip-components=1 -C "$JDK8_HOME"
              rm jdk8.tar.gz

              echo "JDK 8 has been installed locally at $JDK8_HOME"
            else
              echo "JDK 8 is already installed at $JDK8_HOME"
            fi

            # Temporarily switch to JDK 8
            export JAVA_HOME="$JDK8_HOME"
            export PATH="$JAVA_HOME/bin:$PATH"

            echo "Switched to JDK 8"
            java -version

            # Run the specified command here
            cd opensearch-conf
            ./gen-certs-k8.sh
            # Switch back to original JDK
            export JAVA_HOME="$CURRENT_JAVA_HOME"
            export PATH="$ORIGINAL_PATH"

            echo "Switched back to original JDK"
            java -version;;
  n|N|no ) cd opensearch-conf
           ./gen-certs-k8.sh;;
  * ) echo "invalid"
      exit(1);;
esac



cd opensearch-conf
./gen-certs-k8.sh

#set up certificates nifi
cd ..
cd opensearch-conf
cp internal_users.yml.tpl internal_users.yml
cd ..

#kubectl -n $#k8-namespace#$ exec deployment/nifi exec -- bash /opt/nifi/nifi-current/bin/nifi.sh set-single-user-credentials $#nifi-user#$ $#nifi-password#$
echo "new credentials for nifi should have been applied now if no error was shown"
file="nifi/conf/nifi.properties"
#parsing the file
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value} > /dev/null 2>&1
done < "$file"

echo "Truststore password = " ${nifi_security_truststorePasswd}
echo "Keystore password =   " ${nifi_security_keystorePasswd}

sed -i "s|ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB|$#nifi-password#$|" "kubernetes/docker-compose.yml"
sed -i "s|keystorepassword_replace_me|${nifi_security_keystorePasswd}|" "kubernetes/docker-compose.yml"
sed -i "s|truststorepassword_replace_me|${nifi_security_truststorePasswd}|" "kubernetes/docker-compose.yml"

echo "updated nifi in compose file"

