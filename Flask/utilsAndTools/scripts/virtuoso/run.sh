#!bin/bash
#run the virtuoso scripts that would be normally dealt by the post_setup.sh
#these are ran on startup (25s from readiness) of the pod if this file is added to the folder /path/of/your/configuration/servicamap-conf
#you may execute this manually anyway

#!/bin/sh
curl --digest --user dba:$#virtuoso-kb-pwd#$ -X DELETE --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology"

while read p; do
  echo $p
  curl --digest --user dba:$#virtuoso-kb-pwd#$ -X POST --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology" -T "$p"
done < ontologies.list

isql-v localhost dba "$#virtuoso-kb-pwd#$" -H $1 "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');" >> /root/servicemap/out.txt


isql-v localhost dba "$#virtuoso-kb-pwd#$" "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"  >> /root/servicemap/out.txt
isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap.vt >> /root/servicemap/out.txt
isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/valuetypes.vt >> /root/servicemap/out.txt
isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap-dbpedia.vt >> /root/servicemap/out.txt

#an output file will be generated with the results, for debugging reasons
