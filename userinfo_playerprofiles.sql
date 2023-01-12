-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: 127.0.0.1    Database: userinfo
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `playerprofiles`
--

DROP TABLE IF EXISTS `playerprofiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playerprofiles` (
  `Index` int NOT NULL,
  `Org` varchar(45) NOT NULL,
  `User` varchar(45) NOT NULL,
  `Gender` varchar(1) NOT NULL,
  `Weight` double NOT NULL,
  `Height` double NOT NULL,
  PRIMARY KEY (`Index`),
  UNIQUE KEY `Index_UNIQUE` (`Index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playerprofiles`
--

LOCK TABLES `playerprofiles` WRITE;
/*!40000 ALTER TABLE `playerprofiles` DISABLE KEYS */;
INSERT INTO `playerprofiles` VALUES (0,'Senior squad (men)','John Smith','M',75.6,179),(1,'Senior squad (men)','Eric Jones','M',82.1,187),(2,'Senior squad (men)','Jose Alonso','M',70.7,172),(3,'U21 squad (men)','Billy Kidd','M',70.4,180),(4,'U21 squad (men)','Antonio Brown','M',68.5,178),(5,'U21 squad (men)','Josh Hunter','M',71.3,173),(6,'Senior squad (men)','Andre Silva','M',77.4,185);
/*!40000 ALTER TABLE `playerprofiles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-04 12:53:59
