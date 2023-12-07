#!/bin/bash

# copy all iotapp folders, but does not copy over the refresh tokens
find /path/to/source/ -type d -name 'iotapp-*' -exec sh -c 'for dirpath do cp -r --exclude="refresh_token*" "$dirpath" /path/to/destination/; done' sh {} +


# set permissions and create folders given the setup.sh file
grep '^\(chmod\|mkdir\)' /path/to/setup.sh | while IFS= read -r line; do
    echo "$line" # listing lines so that you can see what are you doing
    eval "$line" # this is VERY dangerous, since you can chmod something you shouldn't
done

# copy the opensearch certificates stuff
find /path/to/source/ -type f \( -name '*.p12' -o -name '*.pem' -o ! -name '*.*' -o -name 'internal_users.yml' -o -name '*.srl'\) -exec cp {} /path/to/destination/ \;


# copy the nifi stuff
echo copy paste folder, do not overwrite files and let it paste new files only