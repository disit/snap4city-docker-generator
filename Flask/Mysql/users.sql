CREATE USER 'access_user'@'%' IDENTIFIED BY 'psw_something';
GRANT USAGE ON *.* TO `access_user`@`%`;
GRANT SELECT ON `configurations v-2`.* TO `access_user`@`%`;
GRANT INSERT ON `configurations v-2`.`saved_configurations` TO `access_user`@`%`;
