#!/bin/bash
ANON=$(kubectl exec -n $#k8-namespace#$ deployment/dashboard-builder -- php /var/www/html/dashboardSmartCity/conf/ssl_expose.php)
echo the new anonymous hash is $ANON
