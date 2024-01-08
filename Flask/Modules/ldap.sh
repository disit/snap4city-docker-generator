#!/bin/sh
#generates an hash for the password $#ldap-admin-pwd#$
psw = $(docker-compose exec ldap-server /usr/sbin/slappasswd -h {SSHA} -s "$#ldap-admin-pwd#$")
cd ldap
cp psw_update.ldif psw_update_fixed.ldif
sed -i "s/shaPSW/$psw/g" "psw_update_fixed.ldif"
docker-compose exec ldap-server ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f /ldif_files/psw_update_fixed.ldif
rem psw_update_fixed.ldif
