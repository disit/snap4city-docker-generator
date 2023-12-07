#!/bin/sh
curl --digest --user dba:92NfA0wTMg9RU8V7 -X DELETE --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology"

while read p; do
  echo $p
  curl --digest --user dba:92NfA0wTMg9RU8V7 -X POST --url "http://$1:8890/sparql-graph-crud-auth?graph-uri=http://www.disit.org/km4city/resource/Ontology" -T "$p"
done < ontologies.list

docker-compose exec virtuoso-kb isql-v localhost dba 92NfA0wTMg9RU8V7 -H $1 "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
