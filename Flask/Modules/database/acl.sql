

CREATE TABLE IF NOT EXISTS `Dashboard`.`sessions` (`id` varchar(32) NOT NULL, `access` int(10) unsigned DEFAULT NULL, `data` text, PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS `Dashboard`.`TrustedUserGroups` (`id` INT NOT NULL,`username` VARCHAR(45) NULL, PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `Dashboard`.`AccessDefinitions` (ID INT NOT NULL AUTO_INCREMENT, authname VARCHAR(500) NOT NULL UNIQUE, org TEXT NULL, menuID INT NULL, dashboardID VARCHAR(500) NULL, collectionID VARCHAR(500) NULL, maxbyday INT NULL, maxbymonth INT NULL, maxtotalaccesses INT NULL, PRIMARY KEY (ID));

CREATE TABLE IF NOT EXISTS `Dashboard`.`ACL` (ID INT NOT NULL AUTO_INCREMENT, defID INT NOT NULL, user VARCHAR(500) NOT NULL, PRIMARY KEY (ID), FOREIGN KEY (defID) REFERENCES `Dashboard`.`AccessDefinitions`(ID) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS `Dashboard`.`ACLProfiles` (ID INT NOT NULL AUTO_INCREMENT, profilename VARCHAR(500) NOT NULL UNIQUE, authIDs TEXT NULL, PRIMARY KEY (ID));

CREATE TABLE IF NOT EXISTS `Dashboard`.`ACLProfilesAssignment` (profileID INT NOT NULL, user VARCHAR(500) NOT NULL, PRIMARY KEY (profileID, user), FOREIGN KEY (profileID) REFERENCES `Dashboard`.`ACLProfiles`(ID) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS `Dashboard`.`ACNames` (name VARCHAR(500) NOT NULL, PRIMARY KEY (name));

CREATE TABLE IF NOT EXISTS `DashboardLinkMenu` (`id` int(11) NOT NULL AUTO_INCREMENT, `linkUrl` varchar(300) NOT NULL, `icon` varchar(200) DEFAULT '', `text` varchar(200) DEFAULT '', `openMode` varchar(45) DEFAULT 'newTab', `iconColor` varchar(45) DEFAULT '#FFFFFF', `menuOrder` int(2) DEFAULT 0, `dashboardId` int(11) NOT NULL, PRIMARY KEY (`id`), KEY `DashboardLinkMenu_idfk` (`dashboardId`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT IGNORE INTO `Dashboard`.`ACNames` (name) SELECT profilename FROM `Dashboard`.`ACLProfiles` UNION SELECT authname FROM `Dashboard`.`AccessDefinitions`;

ALTER TABLE `Dashboard`.`ACLProfiles` ADD CONSTRAINT `fk_ACLProfiles_ACNames` FOREIGN KEY (`profilename`) REFERENCES `Dashboard`.`ACNames`(`name`);

ALTER TABLE `Dashboard`.`AccessDefinitions` ADD CONSTRAINT `fk_AccessDefs_ACNames` FOREIGN KEY (`authname`) REFERENCES `Dashboard`.`ACNames`(`name`);

CREATE TABLE IF NOT EXISTS `Dashboard`.`DashboardLinkMenuSubmenus` (`id` int(11) NOT NULL AUTO_INCREMENT, `linkUrl` varchar(300) NOT NULL, `icon` varchar(200) DEFAULT NULL, `text` varchar(200) DEFAULT NULL, `openMode` varchar(45) DEFAULT 'newTab', `iconColor` varchar(45) DEFAULT '#FFFFFF', `menuOrder` int(2) DEFAULT NULL, `menuId` int(11) NOT NULL, `dashboardId` int(11) NOT NULL, PRIMARY KEY (`id`), KEY `DashboardLinkMenuSubmenus_idfk` (`dashboardId`), KEY `DashboardLinkMenuSubmenus_menuidfk` (`menuId`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

ALTER TABLE `Dashboard`.`Config_dashboard` CHANGE COLUMN `subtitle_header` `subtitle_header` VARCHAR(300) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE `Dashboard`.`Config_widget_dashboard` CHANGE COLUMN `title_w` `title_w` VARCHAR(600) CHARACTER SET utf8 COLLATE utf8_general_ci;



INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('Python');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('Rstudio');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('UserStats');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('DataIngestionTable');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('SnapAdvisor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('3DLoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('TPLEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('BIMLoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('ColorMapEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('ODMLoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('VectorFieldLoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('HeatmapProducer');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('SynopticLoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('CSBLEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('DashboardExport');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('DashboardImport');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('GTFSEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('POILoader');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('PythonJupiterHub');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('RouterTool');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('ScenarioEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('SimulationManager');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('SynopticTemplating');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('TLPEditor');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('WidgetExport');
INSERT INTO `Dashboard`.`ACNames` (`name`) VALUES ('WidgetImport');
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('Python', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('Rstudio', 'NULL', 1066);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('UserStats', '*', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('DataIngestionTable', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('SnapAdvisor', '*', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('3DLoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('TPLEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('BIMLoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('ColorMapEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('ODMLoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('VectorFieldLoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('HeatmapProducer', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('SynopticLoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('CSBLEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('DashboardExport', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('DashboardImport', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('GTFSEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('POILoader', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('PythonJupiterHub', '*', 10134);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('RouterTool', '*', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('ScenarioEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('SimulationManager', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('SynopticTemplating', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('TLPEditor', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('WidgetExport', 'NULL', NULL);
INSERT INTO `Dashboard`.`AccessDefinitions` (`authname`, `org`, `menuID`) VALUES ('WidgetImport', 'NULL', NULL);

INSERT INTO `Dashboard`.`MainMenuSubmenus` (`id`, `menu`, `linkUrl`, `linkId`, `icon`, `text`, `privileges`, `userType`, `externalApp`, `openMode`, `iconColor`, `pageTitle`, `menuOrder`, `organizations`) VALUES ('901', '1090', '../management/microApplications.php', 'microApplicationsLink', 'fa fa-dashboard', 'Micro Applications', '[\'RootAdmin\',\'ToolAdmin\', \'AreaManager\', \'Manager\', \'Public\']', 'any', 'no', 'samePage', '#ee41f4', 'Micro Applications', '0', '*');
