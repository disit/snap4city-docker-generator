#!/bin/sh
#generates an hash for the password $#ldap-admin-pwd#$
psw=$(/usr/sbin/slappasswd -h {SSHA} -s "$#ldap-admin-pwd#$")
cp /ldif_files/psw_update.ldif /ldif_files/psw_update_fixed.ldif
# the correct password is placed in the file, which has an invalid placeholder otherwise
sed -i "s@shaPSW@$psw@" "/ldif_files/psw_update_fixed.ldif"
ldapmodify -H ldapi:// -Y EXTERNAL -f /ldif_files/psw_update_fixed.ldif
rm /ldif_files/psw_update_fixed.ldif
ldappasswd -H ldap://localhost -x -D "cn=admin,dc=ldap,dc=organization,dc=com" -w secret -a secret -s $psw