#!/bin/bash

# Function to restore volumes
restore_volume() {
    volume_name=$1
    backup_file="$volume_name.tar.gz"

    if [ -f "$backup_file" ]; then
        docker run --rm -v $volume_name:/$volume_name -v $(pwd):/backup alpine tar -xzvf /backup/$backup_file -C /
        echo "Restored volume: $volume_name"
    else
        echo "Backup file '$backup_file' not found for volume '$volume_name'. Skipping..."
    fi
}

# Loop through each backup file and restore volumes
for backup_file in *.tar.gz
do
    volume_name="${backup_file%.tar.gz}"
    restore_volume $volume_name
done

echo "Volume restoration completed!"
