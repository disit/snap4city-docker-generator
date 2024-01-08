curl -u admin:$#postgre-geo-password#$ -XPOST -H "Content-type: text/xml" -d "<workspace><name>Snap4City</name></workspace>"  http:/$#geoserver-host#$/geoserver/rest/workspaces
