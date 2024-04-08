#!bin/bash
while getopts u:p: flag
do
    case "${flag}" in
        u) username_v=${OPTARG};;
        p) password_v=${OPTARG};;
    esac
done
python3 scripts/modeldevice/modeldevice+synoptics.py $username_v $password_v False