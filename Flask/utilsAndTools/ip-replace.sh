#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Error: Two parameters required."
    echo "Usage: $0 <ip_to_be_replaced> <path_of_folder>"
    exit 1
fi

replacement_string=$1
script_dir=$2

for yaml_file in "$script_dir"/*.yaml; do

    filename=$(basename "$yaml_file")
    if [[ "$filename" == "kafka-deployment-new.yaml" || \
          "$filename" == "kafka-deployment.yaml" || \
          "$filename" == *"persistentvolume.yaml" ]]; then
        echo "Skipping file: $yaml_file"
        continue
    fi

    if [ -e "$yaml_file" ]; then
        echo "Processing file: $yaml_file"
        sed -i "s/127.0.0.1/$replacement_string/g" "$yaml_file"
    else
        echo "No .yaml files found."
    fi
done