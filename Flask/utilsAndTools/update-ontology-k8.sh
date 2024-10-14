#!/bin/sh
curl -sS --digest --user dba:$#virtuoso-kb-pwd#$ -X DELETE --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology"

while read p; do
  echo $p
  curl -sS --digest --user dba:$#virtuoso-kb-pwd#$ -X POST --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology" -T "$p"
done < ontologies.list

if command -v kubectl 2>&1 >/dev/null; then
  kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba $#virtuoso-kb-pwd#$ -H $1 "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
else
  echo no kubectl available
fi

