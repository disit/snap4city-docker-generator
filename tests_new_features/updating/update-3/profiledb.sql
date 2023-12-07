﻿
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

SET NAMES 'utf8';

--
-- Set default database
--
USE profiledb;

--
-- Create view `iot_data_relation`
--
CREATE
VIEW iot_data_relation
AS
SELECT
  `l`.`element_id` AS `id`,
  `l`.`element_type` AS `type`,
  `o1`.`elementName` AS `name`,
  `o`.`elementId` AS `sourceId`,
  `o`.`elementType` AS `sourceType`,
  `o`.`elementName` AS `sourceName`
FROM ((`lightactivity` `l`
  LEFT JOIN `ownership` `o`
    ON ((`o`.`elementId` = CONVERT(`l`.`source_id` USING utf8mb4))))
  LEFT JOIN `ownership` `o1`
    ON (((CONVERT(`l`.`element_id` USING utf8mb4) = `o1`.`elementId`)
    AND ISNULL(`o`.`deleted`))));

--
-- Create index `kpi_id_delete_time_data_time` on table `kpivalues`
--
ALTER TABLE kpivalues 
  ADD INDEX kpi_id_delete_time_data_time(kpi_id, delete_time, data_time);


--
-- Create column `kind` on table `delegation`
--
ALTER TABLE delegation 
  ADD COLUMN kind VARCHAR(25) DEFAULT 'READ_ACCESS';

--
-- Create column `data_time_end` on table `data`
--
ALTER TABLE data 
  ADD COLUMN data_time_end DATETIME DEFAULT NULL;

--
-- Enable foreign keys
--
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;