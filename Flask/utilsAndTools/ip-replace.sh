#!/bin/bash

script_dir=$(dirname "$0")
echo "Enter the replacement string for 127.0.0.1:"
read replacement_string
for yaml_file in "$script_dir"/*.yaml; do

    if [ "$(basename "$yaml_file")" = "kafka-deployment-new.yaml" ]; then
            echo "Skipping file: $yaml_file"
            continue
        fi

    if [ "$(basename "$yaml_file")" = "kafka-deployment.yaml" ]; then
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
