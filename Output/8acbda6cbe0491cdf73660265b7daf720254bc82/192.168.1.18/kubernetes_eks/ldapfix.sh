#!/bin/sh
# for some unexplained reasons ldap server might not have the files in the volumes
# this script reimports the files and folders from the original image

# make the image
kubectl run ldap-server-temp --image=disitlab/preconf-openldap:v3 --restart=Never -n $#k8-namespace#$

#copy the folders
kubectl cp ldap-server-temp:/var/lib/ldap /tmp/ldap/var/lib/ldap -n $#k8-namespace#$
kubectl cp /tmp/ldap/var/lib/ldap ldap-server:/var/lib/ldap -n $#k8-namespace#$
kubectl cp ldap-server-temp:/etc/ldap/slapd.d /tmp/ldap/etc/ldap/slapd.d -n $#k8-namespace#$
kubectl cp /tmp/ldap/etc/ldap/slapd.d ldap-server:/etc/ldap/slapd.d -n $#k8-namespace#$

# apply the new entries in the database
kubectl exec -it deployment/ldap-server-test -n $#k8-namespace#$ -- slapadd -c -v -l /ldif_files/default.ldif

#clean up
kubectl delete pod ldap-server-temp $#k8-namespace#$
rmdir -r /tmp/ldap
