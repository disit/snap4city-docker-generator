# Snap4Sentinel

If you are using the non-containerized version, edit conf.json

Otherwise, edit the environment variables in k8s.yaml

## Setting up users

The script generate_passwords.py will guide you while generating the accounts for Snap4Sentinel

These are then saved in users.txt

There's an existing file which holds the account admin:admin

If you are using the kubernetes version, mount the file on /app/users.txt