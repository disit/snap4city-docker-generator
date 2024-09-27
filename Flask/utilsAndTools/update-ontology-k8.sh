#!/bin/sh
curl --digest --user dba:$#virtuoso-kb-pwd#$ -X DELETE --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology"

while read p; do
  echo $p
  curl --digest --user dba:$#virtuoso-kb-pwd#$ -X POST --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology" -T "$p"
done < ontologies.list

kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba $#virtuoso-kb-pwd#$ -H $1 "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
