CREATE DATABASE  IF NOT EXISTS `checker` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `checker`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: checker
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `asking_containers`
--

DROP TABLE IF EXISTS `asking_containers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asking_containers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` text,
  `log` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1205 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `complex_tests`
--

DROP TABLE IF EXISTS `complex_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complex_tests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_of_test` varchar(100) DEFAULT NULL,
  `command` varchar(200) DEFAULT NULL,
  `extraparameters` varchar(200) DEFAULT NULL,
  `button_color` varchar(7) DEFAULT '#ffffff',
  `explanation` tinytext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_of_test_UNIQUE` (`name_of_test`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complex_tests`
--

LOCK TABLES `complex_tests` WRITE;
/*!40000 ALTER TABLE `complex_tests` DISABLE KEYS */;
INSERT INTO `complex_tests` VALUES (1,'Run setup.sh','bash scripts/run-setup.sh',NULL,'#63c8e9','Calls setup.sh of Snap4City'),
(2,'Run post-setup.sh','bash scripts/run-post-setup.sh',NULL,'#ffffff','Calls post-setup.sh of Snap4City'),
(3,'Read parameters','bash scripts/read_params.sh','string:username:u;number:age:a;string:fullname:f','#000000','This tests simply ensures that passing parameters works'),
(4,'Check iotapps','bash scripts/check_iotapps.sh',NULL,'#20ff14','Check all iotapps, no matter how many they are'),
(5,'Add device','bash scripts/add_device.sh','string:username:u;password:password:p','#ff7f00','Calls the test for adding a new device, then adds some test data'),
(6,'Device creation + synoptics test','bash scripts/modelssynoptics.sh','string:username:u;password:password:p','#ff7f00','Calls the test for adding a new device, adds some test data, while doublechecking with synoptics'),
(7,'Start Containers','bash scripts/launch-containers.sh',NULL,'#7f7f7f',"Attempts to start all containers. Will take time if the images aren't downloaded yet."),
(8,'Check synoptics','bash scripts/synoptics.sh','string:username:u;password:password:p;string:device:d','#ff7f00','Check the synoptics'),
(9,'Check KPI','bash scripts/kpi.sh','string:username:u;password:password:p','#ff7f00','Calls the test for the KPI component'),
(10,'Check Keycloak keys','scripts\keycloakkeys\keycloakkeys.py',NULL,'#0f7f08','Calls the test for the amount of keys in keycloak');
/*!40000 ALTER TABLE `complex_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `getting_tests`
--

DROP TABLE IF EXISTS `getting_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `getting_tests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` text,
  `log` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `rebooting_containers`
--

DROP TABLE IF EXISTS `rebooting_containers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rebooting_containers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` text,
  `log` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rebooting_containers`
--

LOCK TABLES `rebooting_containers` WRITE;
/*!40000 ALTER TABLE `rebooting_containers` DISABLE KEYS */;
INSERT INTO `rebooting_containers` VALUES (4,'2023-10-12 09:47:04','docker restart 33a8aab0e853 resulted in: 33a8aab0e853\n'),(5,'2023-10-12 14:57:12','docker restart 30acc0f82be5 resulted in: 30acc0f82be5\n'),(6,'2023-10-12 15:11:05','docker restart e8535a37b962 resulted in: e8535a37b962\n');
/*!40000 ALTER TABLE `rebooting_containers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_ran`
--

DROP TABLE IF EXISTS `test_ran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_ran` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test` varchar(200) DEFAULT NULL,
  `log` text,
  `date` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_ran`
--

--
-- Table structure for table `tests_results`
--

DROP TABLE IF EXISTS `tests_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tests_results` (
  `id_test` int NOT NULL AUTO_INCREMENT,
  `datetime` text,
  `result` text,
  `container` text,
  `command` text,
  PRIMARY KEY (`id_test`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests_results`
--

LOCK TABLES `tests_results` WRITE;
/*!40000 ALTER TABLE `tests_results` DISABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `tests_table`
--

DROP TABLE IF EXISTS `tests_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tests_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `container_name` varchar(45) DEFAULT NULL,
  `command` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests_table`
--

LOCK TABLES `tests_table` WRITE;
/*!40000 ALTER TABLE `tests_table` DISABLE KEYS */;
INSERT INTO `tests_table` VALUES (2,'opensearch-dashboards','curl -I -s http://localhost:5601/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 302 ] && echo \"Success\" || echo \"Failure\" )'),(3,'proxy','curl -I -s http://localhost/dashboardSmartCity/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 302 ] && echo \"Success\" || echo \"Failure\" )'),(4,'certbot','echo Not meant to be running nor tested'),(5,'dashboard-backend','echo Not meant to be tested'),(6,'dashboard-builder','curl -I -s http://localhost/dashboardSmartCity/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 302 ] && echo \"Success\" || echo \"Failure\" )'),(7,'dashboard-cron','echo Not meant to be tested'),(8,'dashboarddb','if nc -z localhost 3306; then echo \"Success\"; else echo \"Failure\"; fi'),(9,'geoserver','curl -I -s http://localhost:8080/geoserver | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 302 ] && echo \"Success\" || echo \"Failure\" )'),(10,'geoserver-db','if nc -z localhost 5432; then echo \"Success\"; else echo \"Failure\"; fi'),(11,'heatmap-api','echo Not meant to be tested'),(12,'heatmap2geosrv','echo Not meant to be tested'),(14,'iot-fiware-api','curl -I -s http://localhost/iot-directory/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(15,'iot-fiware-harvester','echo Not meant to be tested'),(16,'iotapp-001','curl -I -s http://localhost:1880/iotapp/iotapp-001/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(17,'iotapp-002','curl -I -s http://localhost:1881/iotapp/iotapp-002/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(18,'iotapp-003','curl -I -s http://localhost:1882/iotapp/iotapp-003/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(19,'kafka','string=$(kafkacat -b localhost:9092 -L); if [[ $string == *\"baeldung\"* ]]; then echo \"Success\"; else echo \"Failure\"; fi'),(20,'keycloak','curl -I -s http://localhost/auth/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(21,'ldap-server','if nc -z localhost 389; then echo \"Success\"; else echo \"Failure\"; fi'),(22,'mongo-001','curl -I -s http://localhost:27017/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(23,'myldap','curl -I -s https://myldap:443/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(24,'nifi','curl -I -s --insecure https://localhost:9090 | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failur'),(25,'od-build-api','curl -I -s http://localhost:3000/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 404 ] && echo \"Success\" || echo \"Failure\" )'),(26,'od-get-api','curl -I -s http://localhost:3200/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 404 ] && echo \"Success\" || echo \"Failure\" )'),(27,'od-insert-api','curl -I -s http://localhost:3100/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 404 ] && echo \"Success\" || echo \"Failure\" )'),(28,'od-postgis','if nc -z localhost 5432; then echo \"Success\"; else echo \"Failure\"; fi'),(30,'opensearch-n1','curl -I -s https://localhost:9200/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 401 ] && echo \"Success\" || echo \"Failure\" )'),(31,'orion-001','curl -I -s http://localhost:1026/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 400 ] && echo \"Success\" || echo \"Failure\" )'),(32,'orionbrokerfilter-001','curl -I -s https://localhost:1026/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(33,'personaldata','curl -I -s http://localhost:8080/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 404 ] && echo \"Success\" || echo \"Failure\" )'),(34,'servicemap','curl -I -s http://localhost/ServiceMap/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(35,'solr-kb','curl -I -s http://localhost:8983/solr/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(36,'synoptics','curl -I -s http://localhost/synoptics/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(37,'varnish','curl -I -s http://localhost:6081/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 301 ] && echo \"Success\" || echo \"Failure\" )'),(38,'virtuoso-kb','curl -I -s http://localhost:8890/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 200 ] && echo \"Success\" || echo \"Failure\" )'),(39,'wsserver','curl -I -s http://localhost/wsserver/ | awk \'NR==1{print $2}\' | ( read code && [ \"$code\" -eq 400 ] && echo \"Success\" || echo \"Failure\" )'),(40,'zookeeper','if nc -z localhost 2181; then echo \"Success\"; else echo \"Failure\"; fi');
/*!40000 ALTER TABLE `tests_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'checker'
--
/*!50003 DROP FUNCTION IF EXISTS `GetHighContrastColor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `GetHighContrastColor`(hexColor CHAR(7)) RETURNS char(7) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
  DECLARE colorR INT;
  DECLARE colorG INT;
  DECLARE colorB INT;
  DECLARE colorLuminance DECIMAL(10, 2);
  DECLARE contrastColor CHAR(7);
  DECLARE contrastThreshold INT;
  -- Extract red, green, and blue components from the input color
  SET colorR = CAST(CONV(SUBSTRING(hexColor, 2, 2), 16, 10) AS UNSIGNED);
  SET colorG = CAST(CONV(SUBSTRING(hexColor, 4, 2), 16, 10) AS UNSIGNED);
  SET colorB = CAST(CONV(SUBSTRING(hexColor, 6, 2), 16, 10) AS UNSIGNED);
  SET contrastThreshold = 128;
  -- Calculate luminance for the input color
  SET colorLuminance = 0.2126 * colorR + 0.7152 * colorG + 0.0722 * colorB;

  -- Define the threshold for high contrast (you can adjust this as needed)
  

  -- Choose a contrasting color based on the luminance
  IF colorLuminance > contrastThreshold THEN
    SET contrastColor = '#000000'; -- Black
  ELSE
    SET contrastColor = '#ffffff'; -- White
  END IF;

  RETURN contrastColor;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-02 11:59:11
