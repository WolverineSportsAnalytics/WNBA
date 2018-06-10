-- MySQL Script generated by MySQL Workbench
-- Sun Jun 10 18:18:30 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema wnba_test
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema wnba_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wnba_test` DEFAULT CHARACTER SET utf8 ;
USE `wnba_test` ;

-- -----------------------------------------------------
-- Table `wnba_test`.`dates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wnba_test`.`dates` (
  `iddates` INT(11) NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  PRIMARY KEY (`iddates`),
  UNIQUE INDEX `date_UNIQUE` (`date` ASC),
  INDEX `date_string` (`date` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `wnba_test`.`box_score_urls`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wnba_test`.`box_score_urls` (
  `idboxScoreUrls` INT(11) NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(500) NULL DEFAULT NULL,
  `dateID` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idboxScoreUrls`),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC),
  INDEX `boxScoreDateFK_idx` (`dateID` ASC),
  CONSTRAINT `boxScoreDateFK`
    FOREIGN KEY (`dateID`)
    REFERENCES `wnba_test`.`dates` (`iddates`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `wnba_test`.`player_reference`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wnba_test`.`player_reference` (
  `playerID` INT(11) NOT NULL AUTO_INCREMENT,
  `bbrefID` TEXT NULL DEFAULT NULL,
  `rotogrindersID` INT(11) NULL DEFAULT NULL,
  `fanduelID` TEXT NULL DEFAULT NULL,
  `draftkingsID` INT(11) NULL DEFAULT NULL,
  `rotowireID` INT(11) NULL DEFAULT NULL,
  `firstName` VARCHAR(100) NULL DEFAULT NULL,
  `lastName` VARCHAR(100) NULL DEFAULT NULL,
  `playerName` VARCHAR(100) NULL DEFAULT NULL,
  `team` VARCHAR(45) NULL DEFAULT NULL,
  `nickName` VARCHAR(150) NULL DEFAULT NULL,
  `rotoguruID` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`playerID`),
  UNIQUE INDEX `playerid_UNIQUE` (`playerID` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `wnba_test`.`performance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wnba_test`.`performance` (
  `performanceID` INT(11) NOT NULL AUTO_INCREMENT,
  `playerID` INT(11) NULL DEFAULT NULL,
  `dateID` INT(11) NULL DEFAULT NULL,
  `blocks` INT(11) NULL DEFAULT NULL,
  `points` INT(11) NULL DEFAULT NULL,
  `steals` INT(11) NULL DEFAULT NULL,
  `assists` INT(11) NULL DEFAULT NULL,
  `turnovers` INT(11) NULL DEFAULT NULL,
  `totalRebounds` INT(11) NULL DEFAULT NULL,
  `tripleDouble` INT(11) NULL DEFAULT NULL,
  `doubleDouble` INT(11) NULL DEFAULT NULL,
  `fanduel` INT(11) NULL DEFAULT NULL,
  `draftkings` INT(11) NULL DEFAULT NULL,
  `3PM` INT(11) NULL DEFAULT NULL,
  `offensiveRebounds` INT(11) NULL DEFAULT NULL,
  `defensiveRebounds` FLOAT NULL DEFAULT NULL,
  `minutesPlayed` FLOAT NULL DEFAULT NULL,
  `fieldGoals` INT(11) NULL DEFAULT NULL,
  `fieldGoalsAttempted` INT(11) NULL DEFAULT NULL,
  `fieldGoalPercent` FLOAT NULL DEFAULT NULL,
  `3PA` INT(11) NULL DEFAULT NULL,
  `3PPercent` FLOAT NULL DEFAULT NULL,
  `FT` INT(11) NULL DEFAULT NULL,
  `FTA` INT(11) NULL DEFAULT NULL,
  `FTPercent` FLOAT NULL DEFAULT NULL,
  `personalFouls` INT(11) NULL DEFAULT NULL,
  `plusMinus` INT(11) NULL DEFAULT NULL,
  `trueShootingPercent` FLOAT NULL DEFAULT NULL,
  `effectiveFieldGoalPercent` FLOAT NULL DEFAULT NULL,
  `3pointAttemptRate` FLOAT NULL DEFAULT NULL,
  `freeThrowAttemptRate` FLOAT NULL DEFAULT NULL,
  `offensiveReboundPercent` FLOAT NULL DEFAULT NULL,
  `defensiveReboundPercent` FLOAT NULL DEFAULT NULL,
  `totalReboundPercent` FLOAT NULL DEFAULT NULL,
  `assistPercent` FLOAT NULL DEFAULT NULL,
  `stealPercent` FLOAT NULL DEFAULT NULL,
  `blockPercent` FLOAT NULL DEFAULT NULL,
  `turnoverPercent` FLOAT NULL DEFAULT NULL,
  `usagePercent` FLOAT NULL DEFAULT NULL,
  `offensiveRating` INT(11) NULL DEFAULT NULL,
  `defensiveRating` INT(11) NULL DEFAULT NULL,
  `team` VARCHAR(45) NULL DEFAULT NULL,
  `opponent` VARCHAR(45) NULL DEFAULT NULL,
  `home` INT(11) NULL DEFAULT NULL,
  `fanduelPosition` VARCHAR(45) NULL DEFAULT NULL,
  `draftkingsPosition` VARCHAR(45) NULL DEFAULT NULL,
  `fanduelPts` FLOAT NULL DEFAULT '0',
  `draftkingsPts` FLOAT NULL DEFAULT NULL,
  `simmonsProj` FLOAT NULL DEFAULT NULL,
  `zoProj` FLOAT NULL DEFAULT NULL,
  `hardawayProj` FLOAT NULL DEFAULT NULL,
  `leProj` FLOAT NULL DEFAULT NULL,
  `projMinutes` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`performanceID`),
  INDEX `performanceDate_idx` (`dateID` ASC),
  INDEX `playerPerformance_idx` (`playerID` ASC),
  CONSTRAINT `datePerformance`
    FOREIGN KEY (`dateID`)
    REFERENCES `wnba_test`.`dates` (`iddates`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `playerPerformance`
    FOREIGN KEY (`playerID`)
    REFERENCES `wnba_test`.`player_reference` (`playerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
