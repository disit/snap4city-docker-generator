#!/bin/sh
#generates an hash for the password 4IYJfzNRCwGT0OtM
psw=$(/usr/sbin/slappasswd -h {SSHA} -s "4IYJfzNRCwGT0OtM")
cp /ldif_files/psw_update.ldif /ldif_files/psw_update_fixed.ldif
# the correct password is placed in the file, which has an invalid placeholder otherwise
sed -i "s@shaPSW@$psw@" "/ldif_files/psw_update_fixed.ldif"
ldapmodify -H ldapi:// -Y EXTERNAL -f /ldif_files/psw_update_fixed.ldif
rm /ldif_files/psw_update_fixed.ldif
