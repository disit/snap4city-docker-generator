#!/bin/bash

script_dir=$(dirname "$0")
echo "Enter the replacement string for 127.0.0.1:"
read replacement_string
for yaml_file in "$script_dir"/*.yaml; do

    filename=$(basename "$yaml_file")

    # Skip specific files and files with "persistent-volume" in the name
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