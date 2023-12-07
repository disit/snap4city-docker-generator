DELETE FROM profiledb.`ownership`;
INSERT INTO profiledb.`ownership` VALUES ("1",'userareamanager',"iotapp-001",'AppID','nodered','http://zjyzfjjy/iotapp/001/','{"edgegateway_type":"linux_Linux_4.9.0-8-amd64"}',NULL,'2019-02-19 09:15:00',NULL,NULL),("2",'userareamanager',"iotapp-002",'AppID','nodered','http://zjyzfjjy/iotapp/002/','{"edgegateway_type":"linux_Linux_4.9.0-8-amd64"}',NULL,'2019-02-19 09:15:00',NULL,NULL);
DELETE FROM Dashboard.MainMenuSubmenus WHERE text LIKE "IoT Application nodered%";
INSERT INTO Dashboard.MainMenuSubmenus (menu,linkUrl,linkid,icon,text,privileges,userType,externalApp,openMode,iconColor,pageTitle,menuorder,organizations) VALUES (1035,'http://zjyzfjjy/iotapp/iotapp-001/','iotapp-001','fa fa-file-code-o','IoT Application nodered 001','[\'RootAdmin\', \'AreaManager\']','any','yes','iframe','#FFFFFF','IoT Application nodered 001', 0, '[\'Organization\',\'DISIT\',\'Other\']'),
(1035,'http://zjyzfjjy/iotapp/iotapp-002/','iotapp-002','fa fa-file-code-o','IoT Application nodered 002','[\'RootAdmin\', \'AreaManager\']','any','yes','iframe','#FFFFFF','IoT Application nodered 002', 1, '[\'Organization\',\'DISIT\',\'Other\']'),
('1035', '/iotapp/iotapp-001/ui/#!/0', 'sanity-components', 'fa fa-file-code-o', 'Check components', '[\'RootAdmin\']', 'any', 'yes', 'iframe', '#ffffff', 'Check components', '0', '*'),
('1156', '/phpldapadmin/', 'myLDAP', 'fa fa-users', 'User Role Management', '[\'RootAdmin\']', 'any', 'yes', 'iframe', '#f44242', 'User Role Management', '3', '*');
INSERT INTO `Dashboard`.`MainMenuSubmenus` (`id`, `menu`, `linkUrl`, `linkId`, `icon`, `text`, `privileges`, `userType`, `externalApp`, `openMode`, `iconColor`, `pageTitle`, `menuOrder`) VALUES ('10800', '1059', '/MultiServiceMap/', 'map1link21', 'fa fa-map', 'MultiServiceMap', "['RootAdmin','ToolAdmin', 'AreaManager', 'Manager', 'Public']", 'any', 'any', 'iframe', '#20ff41', 'SuperServiceMap', '2');INSERT INTO profiledb.`ownership` (`username`, `elementId`, `elementType`, `elementName`, `elementUrl`) values('userrootadmin', 'Organization:orion-1','BrokerID','Organization:orion-1','iotbsf');
INSERT INTO iotdb.`contextbroker` (`name`, `protocol`, `ip`, `port`, `uri`, `login`, `password`, `latitude`, `longitude`, `accesslink`, `accessport`, `sha`, `organization`, `apikey`, `visibility`, `version`, `path`, `kind`, `subscription_id`, `urlnificallback`) values('orion-1','ngsi','orion-001','1026',NULL,'login','login','38.685509760012025','-0.720472892345443','orion-broker-filter-001','8443','','Organization',NULL,'private', 'v2', '', 'internal', 'register', 'http://nifi:1030/ingestngsi');

UPDATE Dashboard.MainMenu SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.MainMenuSubmenus SET linkUrl=replace(linkUrl,"http://dashboard/","/");
UPDATE Dashboard.Domains SET domains=replace(domains,"dashboard","zjyzfjjy");
UPDATE Dashboard.Organizations SET kbURL=replace(kbURL,"http://dashboard/","http://zjyzfjjy/");
UPDATE Dashboard.MainMenuSubmenus SET `privileges` = "['RootAdmin','ToolAdmin','AreaManager','Manager']" WHERE (`id` = '10206');
DELETE FROM Dashboard.MainMenuSubmenus WHERE ID=277;
DELETE FROM Dashboard.MainMenu WHERE ID=2004;

DELETE FROM Dashboard.Organizations;
INSERT INTO Dashboard.Organizations VALUES (7,'Organization','http://zjyzfjjy/ServiceMap/api/v1/','38.685509760012025,-0.720472892345443','3','eng','','','','http://virtuoso-kb:8890','','',' ','userareamanager',NULL);
