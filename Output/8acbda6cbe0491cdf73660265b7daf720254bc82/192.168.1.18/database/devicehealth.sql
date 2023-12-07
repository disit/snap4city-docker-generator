-- MySQL Script generated by MySQL Workbench
-- Mon Aug 28 12:00:47 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema notHealthy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema notHealthy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `notHealthy` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `notHealthy` ;

-- -----------------------------------------------------
-- Table `notHealthy`.`Test`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notHealthy`.`Test` (
  `ServiceURI` VARCHAR(250) NOT NULL,
  `Organization` VARCHAR(200) NULL DEFAULT NULL,
  `Broker` VARCHAR(200) NULL DEFAULT NULL,
  `DeviceName` VARCHAR(100) NULL DEFAULT NULL,
  `DeviceModel` VARCHAR(100) NULL DEFAULT NULL,
  `Nature` VARCHAR(45) NULL DEFAULT NULL,
  `Subnature` VARCHAR(45) NULL DEFAULT NULL,
  `VariableName` VARCHAR(100) NULL DEFAULT NULL,
  `VariableValue` VARCHAR(2000) NULL DEFAULT NULL,
  `ExpectedDate` VARCHAR(45) NULL DEFAULT NULL,
  `LastMeasureDate` VARCHAR(45) NULL DEFAULT NULL,
  `FailuresNumber` INT NULL DEFAULT NULL,
  `InsertionTimestamps` INT NULL DEFAULT NULL,
  `Delta` INT NULL DEFAULT NULL,
  `MaxDelta` INT NULL DEFAULT NULL,
  `Percentage` DECIMAL(8,5) NULL DEFAULT NULL
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
