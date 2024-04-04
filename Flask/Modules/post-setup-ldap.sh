echo fixing openldap admin password
docker-compose exec ldap-server bash /ldif_files/psw.sh
