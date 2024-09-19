#!/bin/bash
if [ -z "$1" ]; then
  # get path of this file
  SCRIPT=$(readlink -f "$0")
  # get folder of this file
  SCRIPTPATH=$(dirname "$SCRIPT")
else
  SCRIPTPATH=$1
fi
cd kubernetes
if [ ! -d bkup ]; then
  echo "make backup"
  mkdir bkup
  cp *.yaml bkup
else
  echo "restore yaml files"
  cp bkup/* .
fi
echo "setting shared path for volumes: $SCRIPTPATH"
# replace standard folder with the computed folder
sed -i "s?/mnt/data/generated?$SCRIPTPATH?g" *.yaml
#sed -i "s?/mnt/data/generated?$SCRIPT?g" *.yaml

read -p "create $#k8-namespace#$ namespace? (yes/no) " choice

case "$choice" in
  y|Y|yes ) kubectl create namespace $#k8-namespace#$;;
  n|N|no ) echo "skipping";;
  * ) echo "invalid";;
esac

read -p "run first setup? (yes/no) " choice

case "$choice" in
  y|Y|yes ) ./setup.sh;;
  n|N|no ) echo "skipping";;
  * ) echo "invalid";;
esac

read -p "apply yamls into namaspace $#k8-namespace#$? (yes/no) " choice

case "$choice" in
  y|Y|yes ) kubectl apply -f ../kubernetes --namespace=$#k8-namespace#$;;
  n|N|no ) echo "skipping";;
  * ) echo "invalid";;
esac

read -p "install ngnix ingress controller? (yes/no) " choice

case "$choice" in
  y|Y|yes ) kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml;;
  n|N|no ) echo "skipping";;
  * ) echo "invalid";;
esac

read -p "expose main component to port 80? (yes/no) " choice

case "$choice" in
  y|Y|yes ) kubectl create ingress main-ingress --class=nginx --rule="dashboard-builder/*=dashboard-builder:80";kubectl port-forward --namespace=ingress-nginx service/dashboard-builder 80:80;;
  n|N|no ) echo "skipping";;
  * ) echo "invalid";;
esac
