#!/bin/bash
kubectl -n $#k8-namespace#$ exec deployment/servicemap  --  bash -c "cd /root/servicemap; ./update-ontology-k8.sh virtuoso-kb"
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" "EXEC=rdfs_rule_set ('urn:ontology', 'http://www.disit.org/km4city/resource/Ontology');"
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap.vt
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/valuetypes.vt
kubectl -n $#k8-namespace#$ exec deployment/virtuoso-kb  --  isql-v localhost dba "$#virtuoso-kb-pwd#$" /root/servicemap/servicemap-dbpedia.vt


