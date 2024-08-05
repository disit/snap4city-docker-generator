# Remember to edit the admin password!

To edit the password of userrootadmin, you need replace it in the following locations:

* In the `docker-compose.yaml` file(s)
* In the `personalData.ini` file, inside the `dashboard-builder-conf` folder
* In the nifi flow
* * If you never ran the nifi service, then you may simply uncompress the `flow.xml.gz` file in the `nifi/conf`, manually replace the instance of the password, then compress it back.
* * Otherwise, inside the nifi web UI, you need to disable each component which uses the service `KeycloakTokenProviderControllerService`, then disable the service, and finally you may change the password. Remember to re-enable everything which was disabled.