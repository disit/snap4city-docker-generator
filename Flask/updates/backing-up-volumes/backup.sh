#!/bin/bash

COMPOSE_FILE="$(pwd)/docker-compose.yml"

echo "If the volume names are not properly identified, use 'docker volume ls' to find the radix (it will sort of look like the working folder, if not the exact same), then replace the content of the variable folder name (line 11) to the desired value"

# function to backup volumes
backup_volume() {
    volume_name=$1
	folder_name=$(echo $(basename "$(pwd)") | sed 's/[^a-z0-9_\-]//g') #get the current directory and strip the dots, works perfectly if the hostname was an IP
    docker run --rm -v ${folder_name}_${volume_name}:/${folder_name}_${volume_name} -v $(pwd):/backup alpine tar -czvf /backup/$volume_name.tar.gz /${folder_name}_${volume_name}
}

# get the volumes from docker-compose.yml
volumes=$(docker-compose -f $COMPOSE_FILE config | yq e '.volumes | keys | .[]' -)

# backup loop
for volume in $volumes
do
    echo "Backing up volume: $volume"
    backup_volume $volume
done

echo "Backup completed"
