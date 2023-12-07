#!/bin/sh
FILE=/ready.txt
if [ -f "$FILE" ]; then
    echo "Loading skipped, configuration already completed."
else
    slapadd -c -v -l /ldif_files/default.ldif
    echo "This file exists if the configuration already ran in the past. If you delete this file, the configuration will repeat, with undefined consequences." >> /ready.txt
fi
tail -f /dev/null
