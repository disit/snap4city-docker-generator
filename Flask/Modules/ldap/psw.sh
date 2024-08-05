#!/bin/sh
#generates an hash for the password $#ldap-admin-pwd#$
psw=$(/usr/sbin/slappasswd -h {SSHA} -s "$#ldap-admin-pwd#$")
pswadmin=$(/usr/sbin/slappasswd -h {SSHA} -s "$#dashboard-personaldata-user-pwd#$")
pswaream=$(/usr/sbin/slappasswd -h {SSHA} -s "$#areamanager-pwd#$")
pswuserm=$(/usr/sbin/slappasswd -h {SSHA} -s "$#usermanager-pwd#$")
pswusert=$(/usr/sbin/slappasswd -h {SSHA} -s "$#tool-admin-pwd#$")
cp /ldif_files/psw_update.ldif /ldif_files/psw_update_fixed.ldif
cp /ldif_files/admin_update.ldif /ldif_files/admin_update_fixed.ldif
# the correct password is placed in the file, which has an invalid placeholder otherwise
sed -i "s@shaPSW@$psw@" "/ldif_files/psw_update_fixed.ldif"
sed -i "s@oldUserRootAdminPW@$pswadmin@" "/ldif_files/admin_update_fixed.ldif"
sed -i "s@oldAreaManagerPW@$pswaream@" "/ldif_files/admin_update_fixed.ldif"
sed -i "s@oldUserManagerPW@$pswuserm@" "/ldif_files/admin_update_fixed.ldif"
sed -i "s@oldToolAdminPW@$pswusert@" "/ldif_files/admin_update_fixed.ldif"
ldapmodify -H ldapi:// -Y EXTERNAL -f /ldif_files/psw_update_fixed.ldif
rm /ldif_files/psw_update_fixed.ldif
#ldappasswd -H ldap://localhost -x -D "cn=admin,dc=ldap,dc=organization,dc=com" -w secret -a secret -s $psw