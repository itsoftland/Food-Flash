/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.22-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: my_project_db
-- ------------------------------------------------------
-- Server version	10.6.22-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add vendor',1,'add_vendor'),(2,'Can change vendor',1,'change_vendor'),(3,'Can delete vendor',1,'delete_vendor'),(4,'Can view vendor',1,'view_vendor'),(5,'Can add device',2,'add_device'),(6,'Can change device',2,'change_device'),(7,'Can delete device',2,'delete_device'),(8,'Can view device',2,'view_device'),(9,'Can add order',3,'add_order'),(10,'Can change order',3,'change_order'),(11,'Can delete order',3,'delete_order'),(12,'Can view order',3,'view_order'),(13,'Can add push subscription',4,'add_pushsubscription'),(14,'Can change push subscription',4,'change_pushsubscription'),(15,'Can delete push subscription',4,'delete_pushsubscription'),(16,'Can view push subscription',4,'view_pushsubscription'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add permission',6,'add_permission'),(22,'Can change permission',6,'change_permission'),(23,'Can delete permission',6,'delete_permission'),(24,'Can view permission',6,'view_permission'),(25,'Can add group',7,'add_group'),(26,'Can change group',7,'change_group'),(27,'Can delete group',7,'delete_group'),(28,'Can view group',7,'view_group'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add content type',9,'add_contenttype'),(34,'Can change content type',9,'change_contenttype'),(35,'Can delete content type',9,'delete_contenttype'),(36,'Can view content type',9,'view_contenttype'),(37,'Can add session',10,'add_session'),(38,'Can change session',10,'change_session'),(39,'Can delete session',10,'delete_session'),(40,'Can view session',10,'view_session'),(41,'Can add admin outlet',11,'add_adminoutlet'),(42,'Can change admin outlet',11,'change_adminoutlet'),(43,'Can delete admin outlet',11,'delete_adminoutlet'),(44,'Can view admin outlet',11,'view_adminoutlet'),(45,'Can add vendor menu',12,'add_vendormenu'),(46,'Can change vendor menu',12,'change_vendormenu'),(47,'Can delete vendor menu',12,'delete_vendormenu'),(48,'Can view vendor menu',12,'view_vendormenu'),(49,'Can add vendor advertisement',13,'add_vendoradvertisement'),(50,'Can change vendor advertisement',13,'change_vendoradvertisement'),(51,'Can delete vendor advertisement',13,'delete_vendoradvertisement'),(52,'Can view vendor advertisement',13,'view_vendoradvertisement'),(53,'Can add feedback',14,'add_feedback'),(54,'Can change feedback',14,'change_feedback'),(55,'Can delete feedback',14,'delete_feedback'),(56,'Can view feedback',14,'view_feedback'),(57,'Can add android device',15,'add_androiddevice'),(58,'Can change android device',15,'change_androiddevice'),(59,'Can delete android device',15,'delete_androiddevice'),(60,'Can view android device',15,'view_androiddevice'),(61,'Can add site config',16,'add_siteconfig'),(62,'Can change site config',16,'change_siteconfig'),(63,'Can delete site config',16,'delete_siteconfig'),(64,'Can view site config',16,'view_siteconfig'),(65,'Can add advertisement image',17,'add_advertisementimage'),(66,'Can change advertisement image',17,'change_advertisementimage'),(67,'Can delete advertisement image',17,'delete_advertisementimage'),(68,'Can view advertisement image',17,'view_advertisementimage'),(69,'Can add advertisement profile',18,'add_advertisementprofile'),(70,'Can change advertisement profile',18,'change_advertisementprofile'),(71,'Can delete advertisement profile',18,'delete_advertisementprofile'),(72,'Can view advertisement profile',18,'view_advertisementprofile'),(73,'Can add advertisement profile assignment',19,'add_advertisementprofileassignment'),(74,'Can change advertisement profile assignment',19,'change_advertisementprofileassignment'),(75,'Can delete advertisement profile assignment',19,'delete_advertisementprofileassignment'),(76,'Can view advertisement profile assignment',19,'view_advertisementprofileassignment'),(77,'Can add archived order',20,'add_archivedorder'),(78,'Can change archived order',20,'change_archivedorder'),(79,'Can delete archived order',20,'delete_archivedorder'),(80,'Can view archived order',20,'view_archivedorder');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$C0sy6OhyiqSGpyy2YE6nIX$rNxOeRTckR3rcDT267KlOdC5m/+MXz4AflSrQPBey6A=','2025-06-18 10:56:33.135199',1,'silpc065','','','',1,1,'2025-04-03 05:15:34.261056'),(2,'pbkdf2_sha256$870000$ZfCrZdvM4H81ttjzQKXJwd$A7vlsnNO8HCtFJVhh4AueHyRbx3QWdCcd1ttb1tMirk=','2025-05-19 11:52:10.455319',0,'silpc0651','','','',0,1,'2025-05-16 11:35:15.352361'),(3,'pbkdf2_sha256$870000$4dsmEFMbZLvSPA4tUfbwmp$DJwlqL8HEYEoCke2nhIct0GTsuOVSILw1NLhKozawJQ=',NULL,0,'Starbucks','','','',0,1,'2025-05-16 12:01:51.920916'),(4,'pbkdf2_sha256$870000$Vrxw2pLV38mS40dJH0RiSe$4n1Tc0rW/YdGbTHt9JosiOKHr1hZtcO/DVteT15478s=',NULL,0,'McDonald\'s','','','',0,1,'2025-05-16 12:01:52.495877'),(5,'pbkdf2_sha256$870000$2wFqrwNHfgboBfCrG78xfs$p1XFL0HX4/ZaQoDet8Os7MnoB3OzjxziDRBx/2qRt00=',NULL,0,'KFC','','','',0,1,'2025-05-16 12:01:53.044764'),(6,'pbkdf2_sha256$870000$pxXUtgmqH5dCmNBkAbVX3L$s1glugdViK/755Jt8SOpnH6uV6K+fPvVl7thfo7BSu0=',NULL,0,'Burger King','','','',0,1,'2025-05-16 12:01:53.581988'),(7,'pbkdf2_sha256$870000$czmj3CcH1bzZiWD62Z2Sse$ZuaPzHu8BcoOiPHKq4JQoXCfKfos3XsZb72zSdcgfcM=',NULL,0,'Domino\'s','','','',0,1,'2025-05-16 12:01:54.121187'),(8,'pbkdf2_sha256$870000$se0UqaWJPUPrkd2rThYveO$DelMy8HmkmFHGXO5nvKqcZ5rUUfNE/pn3hxvorCmgs4=',NULL,0,'Pizza Hut','','','',0,1,'2025-05-16 12:01:54.657294'),(9,'pbkdf2_sha256$870000$BN2bnLg0Ws5SkgMlJmpxNV$L5T5mMfHrpEMoZdT7WCKMdwmZSJEbS1EexBGbA1sTSo=',NULL,0,'Subway','','','',0,1,'2025-05-16 12:01:55.193319'),(10,'pbkdf2_sha256$870000$0y8ZhS3duqidONBjj6Tw9u$GLEXeI9oGO73m3uKALM/bnxGzYL+rN7hJ5W9ozyu7dc=',NULL,0,'Costa Coffee','','','',0,1,'2025-05-16 12:01:55.729038'),(11,'pbkdf2_sha256$870000$s0TA0WndfQeX6mmLz06MHW$ZrtUb2ZsGZTrvSw/WfNJTBHZSHpgEYkQARtFfIv35dU=',NULL,0,'silpc06','','','',0,1,'2025-05-16 12:01:56.264377'),(12,'pbkdf2_sha256$870000$XBR5wmlmPEDOLnnupbw9jg$3NZoYCvONY42c8Bpy0Pz+tKZZdtGF8fJ+NeAnZagnU0=','2025-06-09 06:07:40.170124',0,'FoodFlash15','','','',0,1,'2025-05-19 09:27:50.237606'),(13,'pbkdf2_sha256$870000$X1fWWuUeivPuAw7q5eaCBQ$BrHOOlWdPaYuBXP4lLuhiQETZjGSaCxUManvIjqKqZw=','2025-07-01 10:16:40.316633',0,'softlandadmin','','','',0,1,'2025-06-04 04:05:04.097003');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-03 05:31:59.135571','1','Starbucks',1,'[{\"added\": {}}]',11,1),(2,'2025-04-03 05:32:35.544074','2','McDonald\'s',1,'[{\"added\": {}}]',11,1),(3,'2025-04-03 05:33:06.714133','3','KFC',1,'[{\"added\": {}}]',11,1),(4,'2025-04-03 05:34:54.468762','4','Burger King',1,'[{\"added\": {}}]',11,1),(5,'2025-04-03 05:35:29.898189','5','Domino\'s',1,'[{\"added\": {}}]',11,1),(6,'2025-04-03 05:36:09.294679','6','Pizza Hut',1,'[{\"added\": {}}]',11,1),(7,'2025-04-03 05:36:41.472908','7','Subway',1,'[{\"added\": {}}]',11,1),(8,'2025-04-03 05:37:12.128044','8','Costa Coffee',1,'[{\"added\": {}}]',11,1),(9,'2025-04-03 06:02:13.087806','1','Starbucks - Lulu Mall - Starbucks',1,'[{\"added\": {}}]',1,1),(10,'2025-04-03 06:03:50.829908','2','Starbucks - City Square - Starbucks',1,'[{\"added\": {}}]',1,1),(11,'2025-04-03 06:10:59.520549','3','Starbucks - Downtown Plaza - Starbucks',1,'[{\"added\": {}}]',1,1),(12,'2025-04-03 06:12:50.367070','4','McDonald\'s - Lulu Mall - McDonald\'s',1,'[{\"added\": {}}]',1,1),(13,'2025-04-03 06:15:32.019524','4','McDonald\'s - Lulu Mall - McDonald\'s',2,'[{\"changed\": {\"fields\": [\"Location id\"]}}]',1,1),(14,'2025-04-03 06:15:53.966644','4','McDonald\'s - Lulu Mall - McDonald\'s',2,'[{\"changed\": {\"fields\": [\"Vendor id\"]}}]',1,1),(15,'2025-04-03 06:18:48.196952','5','McDonald\'s - Grand Avenue - McDonald\'s',1,'[{\"added\": {}}]',1,1),(16,'2025-04-03 06:20:10.782378','6','McDonald\'s - High Street - McDonald\'s',1,'[{\"added\": {}}]',1,1),(17,'2025-04-03 06:22:05.362019','7','KFC - Lulu Mall - KFC',1,'[{\"added\": {}}]',1,1),(18,'2025-04-03 06:23:27.442382','8','KFC - Mega Mall - KFC',1,'[{\"added\": {}}]',1,1),(19,'2025-04-03 06:25:05.879524','9','KFC - Express Highway - KFC',1,'[{\"added\": {}}]',1,1),(20,'2025-04-03 06:26:38.633098','10','KFC - City Square - KFC',1,'[{\"added\": {}}]',1,1),(21,'2025-04-03 06:28:40.829328','11','Burger King - Lulu Mall - Burger King',1,'[{\"added\": {}}]',1,1),(22,'2025-04-03 06:30:08.702124','12','Domino\'s - Lulu Mall - Domino\'s',1,'[{\"added\": {}}]',1,1),(23,'2025-04-03 06:30:57.261550','13','Pizza Hut - Lulu Mall - Pizza Hut',1,'[{\"added\": {}}]',1,1),(24,'2025-04-03 06:31:55.986293','14','Subway - Lulu Mall - Subway',1,'[{\"added\": {}}]',1,1),(25,'2025-04-03 06:32:40.800411','15','Costa Coffee - Lulu Mall - Costa Coffee',1,'[{\"added\": {}}]',1,1),(26,'2025-04-04 08:43:04.534919','7','KFC - Lulu Mall - KFC',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',1,1),(27,'2025-04-04 08:43:36.131699','1','Starbucks - Lulu Mall - Starbucks',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',1,1),(28,'2025-04-07 06:11:39.363615','5','Token 1',3,'',3,1),(29,'2025-04-07 06:11:39.363655','4','Token 1',3,'',3,1),(30,'2025-04-07 06:11:39.363674','3','Token 1',3,'',3,1),(31,'2025-04-07 06:11:39.363690','2','Token 1',3,'',3,1),(32,'2025-04-07 06:11:39.363704','1','Token 1',3,'',3,1),(33,'2025-04-07 06:15:46.990815','7','Token 1',3,'',3,1),(34,'2025-04-07 06:15:46.990858','6','Token 1',3,'',3,1),(35,'2025-04-07 06:22:17.800370','11','Token 1',3,'',3,1),(36,'2025-04-07 06:22:17.800417','10','Token 1',3,'',3,1),(37,'2025-04-07 06:22:17.800437','9','Token 1',3,'',3,1),(38,'2025-04-07 06:22:17.800453','8','Token 1',3,'',3,1),(39,'2025-04-07 06:34:33.533859','15','Token 1',3,'',3,1),(40,'2025-04-07 06:34:33.533899','14','Token 1',3,'',3,1),(41,'2025-04-07 06:34:33.533919','13','Token 1',3,'',3,1),(42,'2025-04-07 06:34:33.533934','12','Token 1',3,'',3,1),(43,'2025-04-07 08:45:48.983591','1','Subscription for 6eb0ef13-20c9-4dba-ad63-c065bf352877',3,'',4,1),(44,'2025-04-07 08:45:55.348507','19','Token 1',3,'',3,1),(45,'2025-04-07 08:45:55.348560','18','Token 1',3,'',3,1),(46,'2025-04-07 08:45:55.348592','17','Token 1',3,'',3,1),(47,'2025-04-07 08:45:55.348617','16','Token 1',3,'',3,1),(48,'2025-04-07 09:02:25.729137','2','Subscription for 6eb0ef13-20c9-4dba-ad63-c065bf352877',3,'',4,1),(49,'2025-04-07 09:02:32.383325','22','Token 2',3,'',3,1),(50,'2025-04-07 09:02:32.383373','21','Token 1',3,'',3,1),(51,'2025-04-07 09:02:32.383399','20','Token 1',3,'',3,1),(52,'2025-04-08 11:35:23.789606','1','\"device_id\":\"202502CAL050005B\",',1,'[{\"added\": {}}]',2,1),(53,'2025-04-08 11:41:33.102048','1','\"device_id\":\"202502CAL050005B\",',3,'',2,1),(54,'2025-04-08 11:41:51.233269','2','202502CAL050005B',1,'[{\"added\": {}}]',2,1),(55,'2025-04-25 04:15:44.781318','1','Starbucks - Lulu Mall - Starbucks',2,'[]',1,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(7,'auth','group'),(6,'auth','permission'),(8,'auth','user'),(9,'contenttypes','contenttype'),(10,'sessions','session'),(11,'vendors','adminoutlet'),(17,'vendors','advertisementimage'),(18,'vendors','advertisementprofile'),(19,'vendors','advertisementprofileassignment'),(15,'vendors','androiddevice'),(20,'vendors','archivedorder'),(2,'vendors','device'),(14,'vendors','feedback'),(3,'vendors','order'),(4,'vendors','pushsubscription'),(16,'vendors','siteconfig'),(1,'vendors','vendor'),(13,'vendors','vendoradvertisement'),(12,'vendors','vendormenu');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-14 09:56:57.734975'),(2,'auth','0001_initial','2025-03-14 09:57:00.750784'),(3,'admin','0001_initial','2025-03-14 09:57:01.283739'),(4,'admin','0002_logentry_remove_auto_add','2025-03-14 09:57:01.290228'),(5,'admin','0003_logentry_add_action_flag_choices','2025-03-14 09:57:01.295695'),(6,'contenttypes','0002_remove_content_type_name','2025-03-14 09:57:01.760801'),(7,'auth','0002_alter_permission_name_max_length','2025-03-14 09:57:01.972432'),(8,'auth','0003_alter_user_email_max_length','2025-03-14 09:57:02.197727'),(9,'auth','0004_alter_user_username_opts','2025-03-14 09:57:02.204439'),(10,'auth','0005_alter_user_last_login_null','2025-03-14 09:57:02.436521'),(11,'auth','0006_require_contenttypes_0002','2025-03-14 09:57:02.437674'),(12,'auth','0007_alter_validators_add_error_messages','2025-03-14 09:57:02.444193'),(13,'auth','0008_alter_user_username_max_length','2025-03-14 09:57:02.673991'),(14,'auth','0009_alter_user_last_name_max_length','2025-03-14 09:57:02.911584'),(15,'auth','0010_alter_group_name_max_length','2025-03-14 09:57:03.144899'),(16,'auth','0011_update_proxy_permissions','2025-03-14 09:57:03.151045'),(17,'auth','0012_alter_user_first_name_max_length','2025-03-14 09:57:03.380706'),(18,'sessions','0001_initial','2025-03-14 09:57:03.711811'),(19,'webpush','0001_initial','2025-03-14 09:57:04.673517'),(20,'webpush','0002_auto_20190603_0005','2025-03-14 09:57:04.906843'),(21,'webpush','0003_subscriptioninfo_user_agent','2025-03-14 09:57:05.361713'),(22,'webpush','0004_auto_20220831_1500','2025-03-14 09:57:07.408448'),(23,'webpush','0005_auto_20230614_1529','2025-03-14 09:57:09.439633'),(24,'webpush','0006_alter_subscriptioninfo_user_agent','2025-03-14 09:57:09.442562'),(25,'vendors','0001_initial','2025-03-14 09:59:32.783218'),(26,'vendors','0002_vendor_place_id','2025-04-01 03:44:04.208977'),(27,'vendors','0003_alter_order_token_no_alter_order_unique_together','2025-04-01 10:13:02.692628'),(28,'vendors','0004_adminoutlet_vendor_location_id_vendor_logo_and_more','2025-04-03 05:26:40.857160'),(29,'vendors','0005_vendoradvertisement_vendormenu','2025-04-04 10:57:52.559870'),(30,'vendors','0005_vendor_ads_vendor_menus','2025-04-07 04:17:23.857472'),(31,'vendors','0006_feedback','2025-04-10 09:46:09.892918'),(32,'vendors','0007_remove_feedback_order_feedback_vendor','2025-04-10 10:03:08.037469'),(33,'vendors','0008_feedback_category_feedback_feedback_type_and_more','2025-04-22 04:56:15.771841'),(34,'vendors','0009_alter_feedback_category_alter_feedback_feedback_type','2025-04-22 04:56:15.782442'),(35,'vendors','0010_order_notified_at','2025-04-23 12:09:25.461334'),(36,'vendors','0011_order_shown_on_tv','2025-05-06 11:21:05.089892'),(37,'vendors','0012_adminoutlet_customer_address_and_more','2025-05-14 11:53:36.298737'),(38,'vendors','0013_remove_adminoutlet_address_remove_adminoutlet_email_and_more','2025-05-14 12:08:04.240617'),(39,'vendors','0014_adminoutlet_user','2025-05-16 11:31:39.517374'),(40,'vendors','0015_remove_adminoutlet_password_and_more','2025-05-19 07:34:35.323318'),(41,'vendors','0016_adminoutlet_android_apk_count_and_more','2025-05-19 10:06:49.387779'),(42,'vendors','0017_androiddevice','2025-05-20 11:27:06.464330'),(43,'vendors','0018_androiddevice_mac_address','2025-05-22 08:35:57.476465'),(44,'vendors','0019_androiddevice_customer_androiddevice_updated_at_and_more','2025-05-22 08:47:33.557549'),(45,'vendors','0020_alter_order_token_no','2025-05-22 11:00:03.744819'),(46,'vendors','0021_alter_vendor_location_id','2025-05-22 12:20:21.010300'),(47,'vendors','0022_alter_androiddevice_mac_address','2025-05-23 06:34:45.705513'),(48,'vendors','0023_device_customer_alter_device_serial_no_and_more','2025-05-26 07:28:51.469815'),(49,'vendors','0024_rename_customer_device_admin_outlet','2025-05-26 07:31:15.780640'),(50,'vendors','0025_rename_customer_androiddevice_admin_outlet','2025-05-26 07:32:50.353376'),(51,'vendors','0026_alter_order_token_no','2025-05-28 09:40:09.086454'),(52,'vendors','0027_vendor_user','2025-06-02 08:52:01.793267'),(53,'vendors','0028_siteconfig','2025-06-04 05:42:33.783113'),(54,'vendors','0029_vendor_alias_name','2025-06-09 08:48:49.935647'),(55,'vendors','0030_alter_androiddevice_vendor_alter_device_admin_outlet_and_more','2025-06-19 06:00:11.368704'),(56,'vendors','0031_remove_advertisementimage_vendor_and_more','2025-06-19 06:52:49.200953'),(57,'vendors','0032_delete_advertisementimage','2025-06-19 07:00:07.400360'),(58,'vendors','0033_advertisementimage','2025-06-19 07:07:00.402196'),(59,'vendors','0034_advertisementprofile','2025-06-20 08:56:48.007072'),(60,'vendors','0035_advertisementprofile_admin_outlet','2025-06-20 09:46:12.368819'),(61,'vendors','0036_alter_advertisementprofile_admin_outlet','2025-06-20 09:46:54.378670'),(62,'vendors','0037_advertisementprofileassignment','2025-06-24 04:28:51.413700'),(63,'vendors','0038_adminoutlet_auto_delete_hours_and_more','2025-06-30 11:05:07.778043'),(64,'vendors','0039_archivedorder','2025-06-30 11:07:48.055214');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('17mh4os8zg5d1vgvqaxtd4lnc71pnt07','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uGz4c:jwWfvHodGeDpUJXOiA1W0dpQTOuPJUajHl59mtz7DLQ','2025-06-02 11:54:26.720807'),('1cf7k66s0tfgyih3eghgqhgypsqgyj29','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uObWF:59fAiB6ew8SMWYQwyVyQmR68yxnrGo8wpT-EiLjw59I','2025-06-23 12:22:27.683657'),('1htbxa0dcxer1ljys3psf376fqok9pbz','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uWT7Q:jeDFvSEqC2yNZpc3s-PBelJboxliRxrKJTurrrt_U4o','2025-07-15 05:01:20.442893'),('25jkxcskqpnq9d8j8oalc6w2nijsolx7','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSaBu:fFPz-XJzpQj8L_s5sP2pPxoJ6TudgpL7MtMKEPtq6AA','2025-07-04 11:45:54.701704'),('31kef4e2nsiuzkaxypj024vjij8wki1t','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uLycW:CjfRMW_DFzBUNGHq7zENdlh3_UI3pzftGSG6MUx72IQ','2025-06-16 06:26:04.347341'),('3mvyeqi2u5x41oi0dd4fzddw995kbakk','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uCuNr:4HnEbKAI0o8H1MzTZ3S292CfMelRKTZHbNc9jXeF604','2025-05-22 06:05:27.928559'),('4rn0xk9awwrylnqumx79gxdy9vvhiupm','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uOus6:kDlV4A7zsaHE_v-9yjFKuLbO4IOkQ3XUpJGhAeir65A','2025-06-24 09:02:18.315334'),('56xlfxtjy99gz81qk0f4vtm0vwdjvn5j','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uM46s:Tcb8eSPPg5npiC_L43T5_NE-sk9tnE_H5_LOLuB_lHk','2025-06-16 12:17:46.679865'),('5dlzbu9lsmj9wcenlwdgl7a5vitpsime','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uGz5C:3W5BsdIxNkRlLqt0-RyXe_j6gKfzNb75PIpKZGLwT4Q','2025-06-02 11:55:02.490697'),('5gas9qrhsaiqmquwra449o3ifu82yrhq','e30:1uQ05M:9a5wPdwrm8qcyM_tNs4ZFnmCuSCo1T9hQMWFz1BERJg','2025-06-27 08:48:28.872305'),('5kijfhwpp7g6uvj1p6b0aflnzlhpnxoj','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uWWsR:WMc3P0FeZ5VHNJHuDvV0yGQPwYFMCIoj05YZ-sKMVro','2025-07-15 09:02:07.616137'),('5tq5hfyk0ow4e83vlve1wy3fmaasyjed','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uUzt6:3V_r_fiI9EuzjfHcWnC7C2Y3x9J-P4Gfs-XvDrP2D6M','2025-07-11 03:36:28.393384'),('7kvywmxutdfwp2s8lutmi8hbviesz574','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uU2YN:FK5Rz0Hhf1V53nVPsgmrCuUexuYvuXQ2Qpj7lK3Oj2g','2025-07-08 12:15:07.588782'),('8ctnmq5u4jv9e3d4v1ghkx7jvzgn18kk','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uHE9C:GeNCYWlnw0Ap889UDAAzd6rex9_910Bxhp7RnPlyBRA','2025-06-03 04:00:10.778372'),('8dd502l6matl5outejuctpbr39ubk8rf','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uV5dA:L54zP5isaLjAv2u4beCyEmLcENdro5QGhY7RaRCTh3M','2025-07-11 09:44:24.513314'),('8terj8ix6goj6fterz2zock3dlwwl4ym','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uMOiG:VSa2s8K9t9-xWE3X3MGcSAHN9kf1EvUJyfP-wRscqdI','2025-06-17 10:17:44.098147'),('9n5nyucs2moaj1yfy7keioxo23qstw5d','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uMQQo:O1Nsa45s4P_N-auzDb1jg-e1Dz2B3fEKv73MlaP4P_s','2025-06-17 12:07:50.677406'),('anvbfrzha0c0n8i3j0dm0iwttd7gszi2','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uV2vs:GHXMQ9U7uagwEdkOokwAUdVKN9xrj_wBpeeLlMvspMQ','2025-07-11 06:51:32.112115'),('ao6ze28oprqflo0v0ymqk1c8eti3bdnu','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uRqTI:inFgturgtxXOaYPM2JJo-Z5KTqXOam8PHOffIiR5Yyg','2025-07-02 10:56:48.481441'),('aowb1i6w5slc4kjdk0a6aw7vwdwaw88b','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uPHf0:BtOk0MxBnPTnq3jFvVtYCsZrYJNky4ZAlYVpjqQCCQs','2025-06-25 09:22:18.509128'),('axc2d2gk9tsguu6h99mngwys1enxeg2v','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uPenk:wzCkteRnt2_tNEGIHA8WMLJX8tGbt3Zyn5tuQtWP0sA','2025-06-26 10:04:52.326338'),('c4vlex1ycyc9lug5g02j8l323ovdecwf','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uTzDO:UN39etH8tpW77351Fz6UTdrRHDNAhBXHItgezk0XQ6w','2025-07-08 08:41:14.128712'),('cfyumjp1wyglpaow4so8stqmismuwx1d','e30:1uIKVJ:AWwdZcloO1VFyTK52dPz4L9M5h05zDOsHHo9EkUUvxY','2025-06-06 04:59:33.705357'),('cjasmmh9y55q4cin7ur1jaa0bm27f8j5','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u8AGf:WnZgBRoHQwKZi6i5xhIvROAHTA8g2u7cuAPHj6KBVB4','2025-05-09 04:02:25.971905'),('d3r11foppr9wqjizf0x6t3d1yeeenkbn','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u0CvY:LVf4ADuGgMnyfUtM1JK0wAXR4HmWumCHcbTJlmxaUkI','2025-04-17 05:15:44.332461'),('dg7zah9wi400yguipq2wq7og7p70swdp','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uI1iI:uzh4CXL0jre8CihOqonmhPqkcfVku1IbyIynFr0Vq8Y','2025-06-05 08:55:42.298513'),('ek5od33qp6j9ilnfnicb228dig6ax0ug','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uBp50:gbjQBRKog97XKDl7y7FQuUPKbbxpIT7jfiPQtSSOTT8','2025-05-19 06:13:30.484535'),('ep1rwfy5l2r74ayyrh7tk7pb3xfndckj','e30:1uGrMn:F-Srh_GXNYKxoN3Z06hN1S8MCm1T7fptcjQORqBp8Kw','2025-06-02 03:40:41.321292'),('evlo9c9m3toh2vnx1fq1bjbxxkdytq1d','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uM0uH:MqBT07zWqqjbPGHpDOAprfJTNQURk2pQZofZfTzRAm4','2025-06-16 08:52:33.155931'),('g3k3ui7no2d9qy34zcm0w8mo3ppjmikn','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uWBzi:uBbMHcgyvGGHvZu139Pg4SN1yaW-3TZ-pKFfIMvawKw','2025-07-14 10:44:14.570335'),('hgktkw0bzcexdimem94vg6mv6zmvv19v','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uUH0m:Qn_RC3qfUaIqtErBo_OrKvQWpWiZ8oNHKVzMMdPdoYk','2025-07-09 03:41:24.760428'),('igj6u2y9umr4wsulguauxdpaniwfx3h0','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uNUwi:eE8JL8KUPh5dX2VBSKU3ras5JB4tudYSs5RUvKhl_kY','2025-06-20 11:09:12.356889'),('intzwilzgb0m4srw24sshhe5nl5s74h2','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u0fCp:MGy5IS4i8Rh34VfVoJrQZcvwIjFCY92AM2t9hJiaAM0','2025-04-18 11:27:27.955874'),('iy915d2x2huf1cg2l0n0emqh7li7y6d7','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSUNa:byQ1e07I7FwRily95B2A6tTPO8xH4Nn9fGENsb1C0zA','2025-07-04 05:33:34.285537'),('iysv0krqjpe5w8qfge8v434r3xlsophe','e30:1uQ06O:vejjwNkvvpzh1I-4IasajJn2Ndmy77-n5Ot0FJji6A0','2025-06-27 08:49:32.271360'),('iz7ctcb71o8kmd3m03vr7ecqt1ak6r9b','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uOurJ:IFdpueCxy7T6gXC7gvarBN6QJ5Dc8q91rFa-bDLC-7E','2025-06-24 09:01:29.496125'),('ju1j9htmkacf1omrbzm4llfog7bcun27','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSDX8:7p-BvhdKSop98ViDw-VIxL_uRxOBQR_rYmC2tsdncc0','2025-07-03 11:34:18.069623'),('jw0wiq86xx4d2mav1mcufyj3dutyf3y5','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSUZR:ZVD2c1BV3Jt8Xul7JPx2mUXScML4kG5GQQdF2AioFpA','2025-07-04 05:45:49.860853'),('k9taq91hiprs2bbsr4q1rqv5202psmgo','.eJxVjDsOwjAQBe_iGlneJf5R0ucM1npt4wBypDipEHeHSCmgfTPzXiLQttaw9byEKYmLABSn3zESP3LbSbpTu82S57YuU5S7Ig_a5Tin_Lwe7t9BpV6_NTN6MwAZrxgSn8FDTB6Ai-YhG2tddujYaVM8F8OYCBUCRnJotQLx_gABJDeh:1uI3xR:k4CbVm1njx-xCFTHD9cdtosFcra86HPGfkqjTjTai2U','2025-06-05 11:19:29.357549'),('kgtp80bejsjnuebr3gjiaez2b63bnnit','e30:1uGrNR:F_8IHyxMSXf96Ds9L-3rhFKWOM2qZa2jbV3A1OAIZHg','2025-06-02 03:41:21.821853'),('lbk5nw5lg82aqu50z49owipeypgiv8fl','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u25O8:9Z58H7OpXxGT-K8uNu5TJw74LBn7yxFe8-HEmdmcWSk','2025-04-22 09:37:00.622142'),('lyp3xlmi64mslbd39c2dmjhhl7xrudiz','e30:1uPGpl:kUtKSmMgfxg3Y0QrJhEPhc9w5IovmZYv67ecycB1F8w','2025-06-25 08:29:21.642283'),('m9lafyy5r81dd3rjmn1aq8ia6k6em7nj','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uQ0Ri:DiO9IwOv8w_GSN-WQX1hELK8B6nsl0eB9t8QapbotjU','2025-06-27 09:11:34.537285'),('moh2guj5kf8w74vgpn4wrk0eywzevclg','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uTg7n:-UvZuY5q-fNlzUBL9JC1NKN1Unldq0Xopxjss4Swcpg','2025-07-07 12:18:11.940373'),('nah1zqosja1dm9ysmxgf1kgeyhn9a90f','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uUdpB:_XhFq9zAAQkW2Kadi2KRRB4vUaQgmGbvJ2GxJRVuO0I','2025-07-10 04:02:57.593002'),('ntpwwwdubs3onbf8zwg0apbq4h4yfeaj','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uN4oy:QYQwqFYMpTb52lzMiHFZh_TCo9FX84ddDNOPcPKh_tI','2025-06-19 07:15:28.185378'),('p3w4txkpjme696l6d0ncm2ta73hqla0v','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uRO1o:5qa4C2XFcUXLys5y-aBduVNriclV7Wh1XcIK9zTZAEA','2025-07-01 04:34:32.306697'),('pge6zl6y4fwpl4q0j0jnjsfz9mmnu49q','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uPdVC:aZBloeyoQvDjZB-yyKOhbACE6vbKzW5lASU9ldsg82Y','2025-06-26 08:41:38.868640'),('phcokjbbi4tiehjt1a4puz43t1tuz4z9','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uMmik:dYj3G3-WmpLkJIt-RVh4d4lGW3m9kx-q_Rg4hrQHGKQ','2025-06-18 11:55:50.487505'),('ps1tbz07kdjt1x2plb6let5rgj99qrw7','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u0cd8:jRptqGkg0Svi_3rv1orW0ZFfPNec-MHxC223P-vVek8','2025-04-18 08:42:26.743768'),('ps5srd8yonzfj1681bnobm4cfektxzwe','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSV4F:y2tDo6e7V2BrC-xqEQa4yHsjOUb98D-X8PR1S9AlyPg','2025-07-04 06:17:39.947619'),('qarzq804ox09xjk13yuh0wekusmx7g20','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uWY2a:G_aOLW7a66hmZ0XxKvYI9RKcAQkAamAKo30_VAPE6Dg','2025-07-15 10:16:40.321861'),('qherazhlyy6y5s2k9x43wcx4yha9pvwr','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSUQX:XUk3kBctf7hR4hI80lJToqyNSo2Chsp7U3gs0mw28NM','2025-07-04 05:36:37.372745'),('ql22qarlw4eh8vjei7fza43bs8mm0zru','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uW5cm:6ZyqKSpee4mGD1zlWjb7_ZHpfRP1RTj9H-dlwc6YLcM','2025-07-14 03:56:08.330538'),('r7tl0vieyq3784juglof5rsw0oymmd33','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uUgUT:BxR8LMOABAPQLUnxEqJR3Gy1Pw8qiZLGM4qfk4Gi26I','2025-07-10 06:53:45.681788'),('r8ahtnwzozvkdnelefa2d02z5jvckir8','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uFuBa:aAD1aEbTbDdq6mI_s0KnjnLY9w6_Gg2xqqrcZMjIbAc','2025-05-30 12:29:10.108290'),('rhqc19ylebxgcg12wt3iuvf0djvdlc3f','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uTuOM:LMSlWC2oRmW34-yQf6D29YvsSP-P9t5OlYHCzPZtBqA','2025-07-08 03:32:14.121784'),('rp505wiw2u214gus5e63tfiuqjp4i77s','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uUP5e:-iHOnWwPkSpE5UhBVd7O4vAwTZyoyKkOHsW1h9SFgYw','2025-07-09 12:18:58.231783'),('t8lbxruoe67aftvaydlpp790qk5szt5r','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u0dNs:FNj9CRk1yhwC-KZeWC3-hWWSdwhpIznbzaqaHqRHyoA','2025-04-18 09:30:44.104533'),('tn4081zbca8zl4y3vfh6jy0skbny91on','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSU5a:9BMreKgm4Ey4TLAMY3KaSuxCxsMCxkjhWdM_T4mAJi8','2025-07-04 05:14:58.515259'),('twq1svnqplcan60yedpkpvz4frffvrm3','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u1dNm:p3oLSohfrviXYdA_U810r-x09blmKRs8T3dqDBrLcdI','2025-04-21 03:42:46.188760'),('ty59uzipa25or368fbzhcbglrjvyhcqu','.eJxVjEEOwiAQRe_C2hCYAQGX7nsGMh0mUjU0Ke3KeHdt0oVu_3vvv1Smba1567LkqaiLsqhOv-NI_JC2k3Kndps1z21dplHvij5o18Nc5Hk93L-DSr1-62AJXBIHNoBniDYJOsEoKCF6Q8GTEc9oxSVDYBwmZvDRFsSzC6LeH9SKNrA:1uOwCM:FHJ34_c4fw_tlAo1TRmQeqM1YL0cyYf5_IPVJSNXp7k','2025-06-24 10:27:18.790338'),('uh5ljkwq88ltbnxzsi1nj03c1q2t98m3','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uRUb2:_d7L3bvTbaLKxqMke-tmk4Jv9q5kOEvf8Y8EK_KEYLQ','2025-07-01 11:35:20.960306'),('uuesz4aee0edp29oby7xibuc0h3nl6bu','e30:1uQ05h:FyuQqjA-Q31FEDFBl9doEaZAOQGqvE_nr091U1tvyfw','2025-06-27 08:48:49.933998'),('v9jx98ru19mn4b0bupow3zoth6l1a2d5','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uSUKi:S1fHO69O-YiPDPUrX-FxMdI712GAM6Ip1a4XSrSDo9k','2025-07-04 05:30:36.090130'),('w3a7lfarrq80bhc5r7jt1qa62s78c2ul','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1uIQIr:AktsEDa_ilLMftXv7SiZiLjRXkt_qkcLpsfGszKE3hk','2025-06-06 11:11:05.546727'),('ygxxvoelimv0ec68s9oz5oxb9vqs89cv','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uU1uC:7ne7pCxcic6BSiZi4kPWnHx0RaqEknXq8Yz7EiNsbOM','2025-07-08 11:33:36.664667'),('ywtzj93mkdc2k1084cxkj5ckkmw3xbeu','.eJxVjEEOwiAQAP_C2ZAuCxQ8eu8byMJSqRqalPZk_Lsh6UGvM5N5i0DHXsLR8hYWFlcB4vLLIqVnrl3wg-p9lWmt-7ZE2RN52ianlfPrdrZ_g0Kt9K3DGfwAIxqYPXI2Fsl6qzkpJMWgCPWQrEZDSMZoB87kxOjcqICi-HwBrqA2pQ:1u6oRo:LDOMgnZm3G4zBHIauhgXNG8g3QDvIghIW3sq2q_f4ho','2025-05-05 10:32:20.436273'),('zy8yh8fsw7pzxhygkg31bqnkbp13m4ib','.eJxVjjsOwyAQRO9CHSGWhQAp0_sM1npZxc7HSMZUUe4eW3KRtPNmnuatemrr2LcqSz9ldVGA6vQbDsQPmXeS7zTfiuYyr8s06L2iD1p1V7I8r0f3TzBSHbd1ALIuibMQrGcbIQk6wSgoIXpDwZMRzwjikiFrHCZm6yNkxLMLskm51bW8jqPo4fMF5Zw8kQ:1uW702:2ml8D9KFBAaEIZZKlCbXRk27okyGHAWZI6lMGZac_c0','2025-07-14 05:24:14.203984');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_adminoutlet`
--

DROP TABLE IF EXISTS `vendors_adminoutlet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_adminoutlet` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `customer_address` longtext DEFAULT NULL,
  `customer_address2` longtext DEFAULT NULL,
  `customer_city` varchar(100) DEFAULT NULL,
  `customer_contact` varchar(20) DEFAULT NULL,
  `customer_contact_person` varchar(255) DEFAULT NULL,
  `customer_email` varchar(254) DEFAULT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `customer_state` varchar(100) DEFAULT NULL,
  `gst_number` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `android_apk_count` int(11) DEFAULT NULL,
  `android_tv_count` int(11) DEFAULT NULL,
  `authentication_status` varchar(50) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `keypad_device_count` int(11) DEFAULT NULL,
  `led_display_count` int(11) DEFAULT NULL,
  `locations` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`locations`)),
  `outlet_count` int(11) DEFAULT NULL,
  `product_from_date` datetime(6) DEFAULT NULL,
  `product_registration_id` int(11) DEFAULT NULL,
  `product_to_date` datetime(6) DEFAULT NULL,
  `project_code` varchar(100) DEFAULT NULL,
  `total_count` varchar(10) DEFAULT NULL,
  `unique_identifier` varchar(100) DEFAULT NULL,
  `web_login_count` int(11) DEFAULT NULL,
  `auto_delete_hours` int(10) unsigned DEFAULT NULL CHECK (`auto_delete_hours` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `vendors_adminoutlet_user_id_7ae116c6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_adminoutlet`
--

LOCK TABLES `vendors_adminoutlet` WRITE;
/*!40000 ALTER TABLE `vendors_adminoutlet` DISABLE KEYS */;
INSERT INTO `vendors_adminoutlet` VALUES (1,'2025-04-03 05:31:59.132045','2025-05-16 12:01:52.493652','starbucks',NULL,NULL,'9876543210',NULL,'starbucks@gmail.com','Starbucks',NULL,NULL,'9876543210',3,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'2025-04-03 05:32:35.541291','2025-05-16 12:01:53.042646','Mcdonalds',NULL,NULL,'9876543211',NULL,'mcdonalds@gmail.com','McDonald\'s',NULL,NULL,'9876543211',4,NULL,NULL,'Pending',348,NULL,NULL,'\"[{\\\"Kazhakkuttam\\\":\\\"KZ01\\\"},{\\\"Kowdiar\\\":\\\"KW01\\\"},{\\\"Lulu Mall\\\":\\\"LM01\\\"}]\"',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'2025-04-03 05:33:06.712150','2025-05-16 12:01:53.579821','KFC',NULL,NULL,'9876543212',NULL,'kfc@gmail.com','KFC',NULL,NULL,'9876543212',5,NULL,NULL,'Pending',347,NULL,NULL,'\"[{\\\"Kazhakkuttam\\\":\\\"KZ01\\\"},{\\\"Kowdiar\\\":\\\"KW01\\\"},{\\\"Lulu Mall\\\":\\\"LM01\\\"}]\"',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'2025-04-03 05:34:54.466685','2025-05-16 12:01:54.117992','Burger King',NULL,NULL,'9876543213',NULL,'burgerking@gmail.com','Burger King',NULL,NULL,'9876543213',6,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'2025-04-03 05:35:29.895633','2025-05-16 12:01:54.654734','Domino\'s',NULL,NULL,'9876543214',NULL,'dominos@gmail.com','Domino\'s',NULL,NULL,'9876543214',7,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,'2025-04-03 05:36:09.292515','2025-05-16 12:01:55.191193','Pizza Hut',NULL,NULL,'9876543215',NULL,'pizzahut@gmail.com','Pizza Hut',NULL,NULL,'9876543215',8,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'2025-04-03 05:36:41.470971','2025-05-16 12:01:55.726878','Subway',NULL,NULL,'9876543216',NULL,'subway@gmail.com','Subway',NULL,NULL,'9876543216',9,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'2025-04-03 05:37:12.125045','2025-05-16 12:01:56.261556','Costa Coffee',NULL,NULL,'9876543217',NULL,'costacoffee@gmail.com','Costa Coffee',NULL,NULL,'9876543217',10,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(16,'2025-05-16 04:28:26.609762','2025-05-16 12:01:56.799867','address 1','address 2','state','9567111111','contact person','com@email.com','food flash5','city','GST123546854695','9567000000',11,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,'2025-05-16 05:53:01.773778','2025-05-16 11:35:15.926750','address 1','address 2','state','9567111111','contact person','aacom@email.com','Food Flash10','city','GST123546854695','9567000000',2,NULL,NULL,'Pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,'2025-05-19 09:27:50.851765','2025-05-20 04:02:07.568519','address 1','address 2','city','9567111111','contact person','foodflash15@email.com','FoodFlash15','state','GST123542865482','9567000000',12,1,1,'Approve',400,1,2,'\"[{\\\"Kazhakkuttam\\\":\\\"KZ01\\\"},{\\\"Kowdiar\\\":\\\"KW01\\\"},{\\\"Lulu Mall\\\":\\\"LM01\\\"}]\"',2,'2025-05-18 18:30:00.000000',338,'2025-05-30 18:30:00.000000','FOODFLASHQC','5','338101747646867',2,NULL),(19,'2025-06-04 04:05:04.707750','2025-07-01 12:31:05.310596','Kinfra','Menamkulam','Trivandrum','9865856574','Prashanth','softland@gmail.com','Softland Food Flash','Kerala','GST458465742458','5685457415',13,1,2,'Approve',351,1,2,'\"[{\\\"Kazhakkuttam\\\":\\\"KZ01\\\"},{\\\"Kowdiar\\\":\\\"KW01\\\"},{\\\"Lulu Mall\\\":\\\"LM01\\\"},{\\\"Trivandrum\\\":\\\"VAZ01\\\"}]\"',2,'2025-06-03 18:30:00.000000',342,'2026-01-30 18:30:00.000000','FOODFLASHQC','5','34251749009902',2,2);
/*!40000 ALTER TABLE `vendors_adminoutlet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_advertisementimage`
--

DROP TABLE IF EXISTS `vendors_advertisementimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_advertisementimage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `admin_outlet_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_advertisemen_admin_outlet_id_bd2b5d50_fk_vendors_a` (`admin_outlet_id`),
  CONSTRAINT `vendors_advertisemen_admin_outlet_id_bd2b5d50_fk_vendors_a` FOREIGN KEY (`admin_outlet_id`) REFERENCES `vendors_adminoutlet` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_advertisementimage`
--

LOCK TABLES `vendors_advertisementimage` WRITE;
/*!40000 ALTER TABLE `vendors_advertisementimage` DISABLE KEYS */;
INSERT INTO `vendors_advertisementimage` VALUES (75,'ads/SOFTLAND1_MqX0usp.jpg','2025-06-20 04:40:16.533806',19),(76,'ads/SOFTLAND2_GrcJ5ea.jpg','2025-06-20 04:40:16.534704',19),(77,'ads/SOFTLAND3_Id2RZsG.jpg','2025-06-20 04:40:16.535677',19),(78,'ads/SOFTLAND4_CfXTu9i.jpg','2025-06-20 04:40:16.536528',19),(79,'ads/SOFTLAND2_i88P3AQ.jpg','2025-06-20 04:40:22.399627',19),(80,'ads/SOFTLAND3_Cq9lPKm.jpg','2025-06-20 04:40:22.402634',19),(87,'ads/SOFTLAND1_eIy2dCQ.jpg','2025-06-24 05:42:09.617514',19),(88,'ads/SOFTLAND2_FNkRJGn.jpg','2025-06-24 05:42:09.618695',19),(89,'ads/SOFTLAND3_yVZPOd9.jpg','2025-06-24 05:42:09.619706',19),(90,'ads/SOFTLAND4_RWBwnag.jpg','2025-06-24 05:42:09.620642',19),(96,'ads/WEEKEND1.jpg','2025-06-30 04:43:34.770545',19),(97,'ads/WEEKEND2.jpg','2025-06-30 04:43:34.770833',19),(98,'ads/WEEKEND3.jpg','2025-06-30 04:43:34.771075',19),(99,'ads/WEEKEND4.jpg','2025-06-30 04:43:34.771310',19),(100,'ads/WEEKEND5.jpg','2025-06-30 04:43:34.771540',19),(101,'ads/WEEKDAY2.jpg','2025-06-30 04:55:27.744269',19),(102,'ads/WEEKDAY1.jpg','2025-06-30 04:55:27.744601',19),(103,'ads/WEEKDAY3.jpg','2025-06-30 04:55:27.744901',19),(104,'ads/WEEKDAY4.jpg','2025-06-30 04:55:27.745165',19),(105,'ads/WEEKDAY5.jpg','2025-06-30 04:55:27.745456',19);
/*!40000 ALTER TABLE `vendors_advertisementimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_advertisementprofile`
--

DROP TABLE IF EXISTS `vendors_advertisementprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_advertisementprofile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `days_active` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`days_active`)),
  `priority` smallint(5) unsigned NOT NULL CHECK (`priority` >= 0),
  `created_at` datetime(6) NOT NULL,
  `admin_outlet_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_advertisemen_admin_outlet_id_2d71857b_fk_vendors_a` (`admin_outlet_id`),
  CONSTRAINT `vendors_advertisemen_admin_outlet_id_2d71857b_fk_vendors_a` FOREIGN KEY (`admin_outlet_id`) REFERENCES `vendors_adminoutlet` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_advertisementprofile`
--

LOCK TABLES `vendors_advertisementprofile` WRITE;
/*!40000 ALTER TABLE `vendors_advertisementprofile` DISABLE KEYS */;
INSERT INTO `vendors_advertisementprofile` VALUES (32,'WEEKEND OFFERS',NULL,NULL,'[\"Saturday\", \"Sunday\"]',2,'2025-06-30 04:44:29.827152',19),(33,'WEEKDAY OFFERS',NULL,NULL,'[\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\"]',3,'2025-06-30 04:56:07.863964',19);
/*!40000 ALTER TABLE `vendors_advertisementprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_advertisementprofile_images`
--

DROP TABLE IF EXISTS `vendors_advertisementprofile_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_advertisementprofile_images` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `advertisementprofile_id` bigint(20) NOT NULL,
  `advertisementimage_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_advertisementpro_advertisementprofile_id__95d3776d_uniq` (`advertisementprofile_id`,`advertisementimage_id`),
  KEY `vendors_advertisemen_advertisementimage_i_259f17d4_fk_vendors_a` (`advertisementimage_id`),
  CONSTRAINT `vendors_advertisemen_advertisementimage_i_259f17d4_fk_vendors_a` FOREIGN KEY (`advertisementimage_id`) REFERENCES `vendors_advertisementimage` (`id`),
  CONSTRAINT `vendors_advertisemen_advertisementprofile_112d50ab_fk_vendors_a` FOREIGN KEY (`advertisementprofile_id`) REFERENCES `vendors_advertisementprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_advertisementprofile_images`
--

LOCK TABLES `vendors_advertisementprofile_images` WRITE;
/*!40000 ALTER TABLE `vendors_advertisementprofile_images` DISABLE KEYS */;
INSERT INTO `vendors_advertisementprofile_images` VALUES (59,32,96),(60,32,97),(61,32,98),(62,32,99),(63,32,100),(64,33,101),(65,33,102),(66,33,103),(67,33,104),(68,33,105);
/*!40000 ALTER TABLE `vendors_advertisementprofile_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_advertisementprofileassignment`
--

DROP TABLE IF EXISTS `vendors_advertisementprofileassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_advertisementprofileassignment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `assigned_at` datetime(6) NOT NULL,
  `profile_id` bigint(20) NOT NULL,
  `vendor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_advertisementpro_profile_id_vendor_id_0b81ccf1_uniq` (`profile_id`,`vendor_id`),
  KEY `vendors_advertisemen_vendor_id_8de5c705_fk_vendors_v` (`vendor_id`),
  CONSTRAINT `vendors_advertisemen_profile_id_a1d4a532_fk_vendors_a` FOREIGN KEY (`profile_id`) REFERENCES `vendors_advertisementprofile` (`id`),
  CONSTRAINT `vendors_advertisemen_vendor_id_8de5c705_fk_vendors_v` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_advertisementprofileassignment`
--

LOCK TABLES `vendors_advertisementprofileassignment` WRITE;
/*!40000 ALTER TABLE `vendors_advertisementprofileassignment` DISABLE KEYS */;
INSERT INTO `vendors_advertisementprofileassignment` VALUES (25,'2025-06-30 05:54:00.659264',33,51);
/*!40000 ALTER TABLE `vendors_advertisementprofileassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_androiddevice`
--

DROP TABLE IF EXISTS `vendors_androiddevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_androiddevice` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) DEFAULT NULL,
  `mac_address` varchar(255) DEFAULT NULL,
  `admin_outlet_id` bigint(20) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `vendors_androiddevice_mac_address_d10d5c97_uniq` (`mac_address`),
  KEY `vendors_androiddevice_vendor_id_82878d1a_fk_vendors_vendor_id` (`vendor_id`),
  KEY `vendors_androiddevic_admin_outlet_id_06a65dad_fk_vendors_a` (`admin_outlet_id`),
  CONSTRAINT `vendors_androiddevic_admin_outlet_id_06a65dad_fk_vendors_a` FOREIGN KEY (`admin_outlet_id`) REFERENCES `vendors_adminoutlet` (`id`),
  CONSTRAINT `vendors_androiddevice_vendor_id_82878d1a_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_androiddevice`
--

LOCK TABLES `vendors_androiddevice` WRITE;
/*!40000 ALTER TABLE `vendors_androiddevice` DISABLE KEYS */;
INSERT INTO `vendors_androiddevice` VALUES (2,'dgPSXmLVRoO_yi2x0Md5WM:APA91bHNIHZ-OAMakBts-lRqSDlM-ed8Q97tiiFhbwG-IWjKZKIZtcYJ69CYsc5uS6_bs38zx5E6wikHZQ6LHWjtEwHS1oYKGhDq7nv_cfNWSQ9qjDeQUM0','2025-05-22 05:23:22.335146',51,'528328432a57fa5f',19,'2025-06-26 11:57:33.728474'),(3,'ceZhDy8BRGKNZfNHmYYnop:APA91bGg26sMAiVMbodrK8Wmv-bJ6XiwfHEXjdDU7KcQXT8xhvC3r8fBgb7h8plLXwRWacmFmn7rwWj1bDxsaQ3rp6P2LbD98kB8bgGKrbVOyrUnDWnkSj0','2025-05-22 06:39:04.730181',16,'528328432a57fa5',3,'2025-05-23 05:57:30.245530'),(15,'cPXhj6hARimTgkLRyVBMRS:APA91bHDTYGRoKg0c_sGi0REp0DtIjF6fWIJ5bQeekgvkX9W6K4Nc-bp2DR7UgcYC0wP9hB5snZW1xiU0c_xdZVpOGXGzYdsQ1G0wWDJ5Dqegg','2025-06-04 10:08:52.395818',NULL,'528328432a57331',19,'2025-06-26 09:26:54.534379'),(16,'cPXhj6hARimTgkLRyVBMRS:APA91bHDTYGRoKg0c_sGi0REp0DtIjF6fWIJ5bQeekgvkX9W6K4Nc-bp2DR7UgcYC0wP9hB5snZW1xiU0c_xdZVpOGXGzYdsQ1G0wWDJ5Dqeg','2025-06-04 10:08:58.637242',NULL,'528328432a57687',19,'2025-06-09 06:44:24.458298'),(17,'ffU_wlLiT2O25ZTNfxfow0:APA91bEbHLCWZME9w32IvNxydXEFItNp9B_owtBZK1erhcSHH5K1BgEyDCwgoPzuGNPPTBsBYiIj2HY4aXqcSbGtkHd2_xf-XhjhYH2_U3oqkrL5CkZFCVs','2025-06-05 06:57:11.581275',51,'b2de5585738c1d97',19,'2025-06-26 11:57:33.730918'),(18,'cVKGVjO4RtWA3UZo_r_L6o:APA91bEFJoZm7hKol6iC5eI7dF2N4LLs0NKBgmLWCAf-ZxJt4mx-CTGbcjoQKMiY-5PVc44EtpccXCIcGJwoznovumlXTpeYlbVb40Y9bZm6qVuzdMiUXj0','2025-06-05 07:11:38.764998',51,'9638f60866f4de64',19,'2025-06-26 11:57:33.732922'),(19,'fon6aPv9Qcud9FF-yuO0yf:APA91bFPJAUPlmeHOCOEH9URTkGAAF551KxwpBqMRyreM6R8O1_hlWGgdl28YDpNEc3dIeKehlVbz8wHsLY5sJL78qZAPZLes_H6fb0XVBGNKoDDN22ROp8','2025-06-09 10:27:27.514200',63,'8c0482bbb37ae9b8',19,'2025-06-18 07:18:47.990477');
/*!40000 ALTER TABLE `vendors_androiddevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_archivedorder`
--

DROP TABLE IF EXISTS `vendors_archivedorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_archivedorder` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `original_order_id` int(11) NOT NULL,
  `token_no` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `counter_no` int(11) NOT NULL,
  `shown_on_tv` tinyint(1) NOT NULL,
  `notified_at` datetime(6) DEFAULT NULL,
  `updated_by` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `archived_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_archivedorder_vendor_id_f0413203_fk_vendors_vendor_id` (`vendor_id`),
  CONSTRAINT `vendors_archivedorder_vendor_id_f0413203_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_archivedorder`
--

LOCK TABLES `vendors_archivedorder` WRITE;
/*!40000 ALTER TABLE `vendors_archivedorder` DISABLE KEYS */;
INSERT INTO `vendors_archivedorder` VALUES (1,1369,1,'ready',1,0,'2025-06-30 12:04:06.048405','client','2025-06-30 11:17:04.404396','2025-06-30 12:04:05.704814','2025-07-01 05:28:27.360477',51),(2,1370,2,'ready',1,0,'2025-06-30 12:04:36.545445','client','2025-06-30 11:17:06.299708','2025-06-30 12:04:36.246091','2025-07-01 05:28:27.374262',51),(3,1371,3,'ready',1,0,'2025-07-01 05:12:18.134912','client','2025-06-30 11:17:07.035436','2025-07-01 05:12:17.786048','2025-07-01 05:28:27.385008',51),(4,1372,4,'ready',1,0,'2025-06-30 12:04:45.122416','client','2025-06-30 11:17:07.867511','2025-06-30 12:04:44.835435','2025-07-01 05:28:27.415766',51),(5,1373,5,'ready',1,0,'2025-06-30 12:04:46.792964','client','2025-06-30 11:17:08.332939','2025-06-30 12:04:46.501766','2025-07-01 05:28:27.446396',51),(6,1374,6,'ready',1,0,'2025-06-30 12:04:48.386518','client','2025-06-30 11:17:08.763611','2025-06-30 12:04:48.098045','2025-07-01 05:28:27.466586',51),(7,1375,57,'ready',1,0,'2025-06-30 12:01:26.092505','client','2025-06-30 12:01:26.083636','2025-06-30 12:01:26.083669','2025-07-01 05:28:27.483874',51),(8,1376,60,'ready',1,0,'2025-06-30 12:01:27.553106','client','2025-06-30 12:01:27.544371','2025-06-30 12:01:27.544423','2025-07-01 05:28:27.492844',51),(9,1377,56,'ready',1,0,'2025-06-30 12:01:29.063510','client','2025-06-30 12:01:29.054570','2025-06-30 12:01:29.054601','2025-07-01 05:28:27.501246',51),(10,1378,7,'ready',1,0,'2025-06-30 12:04:49.901104','client','2025-06-30 12:04:49.887001','2025-06-30 12:04:49.887048','2025-07-01 05:28:27.510211',51),(11,1379,1,'ready',1,0,'2025-07-01 06:54:27.990573','client','2025-07-01 06:14:04.677946','2025-07-01 06:54:27.691120','2025-07-01 08:18:11.243091',51),(12,1380,2,'ready',1,0,'2025-07-01 06:21:33.136041','client','2025-07-01 06:21:33.130759','2025-07-01 06:21:33.130787','2025-07-01 08:23:11.246298',51),(13,1381,3,'ready',1,0,'2025-07-01 06:21:34.735159','client','2025-07-01 06:21:34.721047','2025-07-01 06:21:34.721122','2025-07-01 08:23:11.262883',51),(14,1382,4,'ready',1,0,'2025-07-01 06:21:36.259698','client','2025-07-01 06:21:36.253775','2025-07-01 06:21:36.253805','2025-07-01 08:23:11.279159',51),(15,1383,5,'ready',1,0,'2025-07-01 06:21:37.733489','client','2025-07-01 06:21:37.727699','2025-07-01 06:21:37.727721','2025-07-01 08:23:11.294138',51),(16,1384,6,'ready',1,0,'2025-07-01 06:21:39.170299','client','2025-07-01 06:21:39.165495','2025-07-01 06:21:39.165518','2025-07-01 08:23:11.310032',51),(17,1385,7,'ready',1,0,'2025-07-01 06:21:40.637913','client','2025-07-01 06:21:40.625236','2025-07-01 06:21:40.625303','2025-07-01 08:23:11.326405',51),(18,1386,8,'ready',1,0,'2025-07-01 06:21:42.146485','client','2025-07-01 06:21:42.140457','2025-07-01 06:21:42.140492','2025-07-01 08:23:11.341930',51),(19,1387,9,'ready',1,0,'2025-07-01 06:21:43.587484','client','2025-07-01 06:21:43.577359','2025-07-01 06:21:43.577436','2025-07-01 08:23:11.357244',51),(20,1388,10,'ready',1,0,'2025-07-01 06:21:45.053046','client','2025-07-01 06:21:45.041930','2025-07-01 06:21:45.042017','2025-07-01 08:23:11.373656',51),(21,1389,1,'ready',4,0,'2025-07-01 09:42:37.414482','client','2025-07-01 09:42:37.387255','2025-07-01 09:42:37.387333','2025-07-01 11:46:12.309867',51);
/*!40000 ALTER TABLE `vendors_archivedorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_device`
--

DROP TABLE IF EXISTS `vendors_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_device` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `serial_no` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) DEFAULT NULL,
  `admin_outlet_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_device_serial_no_de192fef_uniq` (`serial_no`),
  KEY `vendors_device_vendor_id_80d1e485_fk_vendors_vendor_id` (`vendor_id`),
  KEY `vendors_device_admin_outlet_id_e7d9c09b_fk_vendors_a` (`admin_outlet_id`),
  CONSTRAINT `vendors_device_admin_outlet_id_e7d9c09b_fk_vendors_a` FOREIGN KEY (`admin_outlet_id`) REFERENCES `vendors_adminoutlet` (`id`),
  CONSTRAINT `vendors_device_vendor_id_80d1e485_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_device`
--

LOCK TABLES `vendors_device` WRITE;
/*!40000 ALTER TABLE `vendors_device` DISABLE KEYS */;
INSERT INTO `vendors_device` VALUES (2,'202502CAL000005B','2025-04-08 11:41:51.232254','2025-05-22 12:20:53.486992',7,2),(3,'202505FDF000002B','2025-05-29 03:44:30.249373','2025-06-26 11:57:33.719987',51,19),(10,'202505CAL000002B','2025-06-04 10:04:05.706632','2025-06-09 06:44:24.455427',NULL,19),(11,'202505CAL000004B','2025-06-04 10:04:08.162095','2025-06-09 06:36:02.078292',NULL,19),(12,'202505CAL000001B','2025-06-04 10:09:05.682153','2025-06-26 09:26:54.525039',NULL,19),(13,'202505CAL000003B','2025-06-06 07:39:57.571710','2025-06-26 11:57:33.724440',51,19),(14,'202502CAL050005B','2025-06-09 05:45:47.900849','2025-06-18 07:18:47.986255',63,19),(15,'202505CRN000006B','2025-06-11 05:34:05.735005','2025-06-18 07:18:47.987982',63,19);
/*!40000 ALTER TABLE `vendors_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_feedback`
--

DROP TABLE IF EXISTS `vendors_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_feedback` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) NOT NULL,
  `category` varchar(10) DEFAULT NULL,
  `feedback_type` varchar(10) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `want_to_reach_us` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_feedback_vendor_id_837b76c5_fk_vendors_vendor_id` (`vendor_id`),
  CONSTRAINT `vendors_feedback_vendor_id_837b76c5_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_feedback`
--

LOCK TABLES `vendors_feedback` WRITE;
/*!40000 ALTER TABLE `vendors_feedback` DISABLE KEYS */;
INSERT INTO `vendors_feedback` VALUES (3,'1','2025-04-23 10:23:18.945960',7,NULL,NULL,NULL,0),(4,'1','2025-04-23 10:57:12.237535',7,NULL,NULL,NULL,0),(5,'ee','2025-05-13 09:40:52.945084',7,NULL,NULL,NULL,0),(6,'good','2025-05-13 09:42:52.502816',7,NULL,NULL,NULL,0),(7,'good','2025-05-13 09:42:58.736002',7,NULL,NULL,NULL,0),(8,'good','2025-05-13 09:43:00.095196',7,NULL,NULL,NULL,0),(9,'good','2025-05-13 09:43:17.657526',7,NULL,NULL,NULL,0),(10,'good','2025-05-13 09:45:30.203269',7,NULL,NULL,NULL,0),(11,'a','2025-05-13 10:15:54.170882',7,NULL,NULL,NULL,0),(12,'a','2025-05-13 10:16:03.428243',7,NULL,NULL,NULL,0),(13,'a','2025-05-13 10:18:18.155996',7,NULL,NULL,NULL,0),(14,'a','2025-05-13 10:18:22.014307',7,NULL,NULL,NULL,0),(15,'s','2025-05-13 10:24:57.610613',7,NULL,NULL,NULL,0),(16,'a','2025-05-13 10:35:57.095866',7,NULL,NULL,NULL,0),(17,'a','2025-05-13 10:46:30.155908',7,NULL,NULL,NULL,0),(18,'a','2025-05-13 10:48:04.998228',7,NULL,NULL,NULL,0),(19,'ashik is  good','2025-05-13 11:01:09.845327',7,NULL,NULL,NULL,0),(20,'qq','2025-05-13 11:04:15.547777',7,NULL,NULL,NULL,0),(21,'aa','2025-05-13 11:08:00.962247',7,NULL,NULL,NULL,0),(22,'zz','2025-05-13 11:12:15.449556',7,'dish','complaint','q',0),(23,'good','2025-05-13 11:14:23.291607',7,'service','suggestion','amal',0),(24,'q','2025-05-13 11:20:06.194327',7,'dish','suggestion','q',0),(25,'\'','2025-05-13 11:22:49.980183',7,'dish','complaint','',0),(26,'aaaa.','2025-05-13 11:35:29.056609',7,'dish','complaint','1',0);
/*!40000 ALTER TABLE `vendors_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_order`
--

DROP TABLE IF EXISTS `vendors_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token_no` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `counter_no` int(11) NOT NULL,
  `updated_by` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `vendor_id` bigint(20) NOT NULL,
  `notified_at` datetime(6) DEFAULT NULL,
  `shown_on_tv` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_order_token_no_vendor_id_72312e63_uniq` (`token_no`,`vendor_id`),
  KEY `vendors_order_device_id_19b98022_fk_vendors_device_id` (`device_id`),
  KEY `vendors_order_vendor_id_a6e689bb_fk_vendors_vendor_id` (`vendor_id`),
  CONSTRAINT `vendors_order_device_id_19b98022_fk_vendors_device_id` FOREIGN KEY (`device_id`) REFERENCES `vendors_device` (`id`),
  CONSTRAINT `vendors_order_vendor_id_a6e689bb_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`),
  CONSTRAINT `token_no_range` CHECK (`token_no` between 0 and 9999)
) ENGINE=InnoDB AUTO_INCREMENT=1390 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_order`
--

LOCK TABLES `vendors_order` WRITE;
/*!40000 ALTER TABLE `vendors_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_pushsubscription`
--

DROP TABLE IF EXISTS `vendors_pushsubscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_pushsubscription` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `browser_id` varchar(255) NOT NULL,
  `endpoint` longtext NOT NULL,
  `p256dh` longtext NOT NULL,
  `auth` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `browser_id` (`browser_id`),
  UNIQUE KEY `endpoint` (`endpoint`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_pushsubscription`
--

LOCK TABLES `vendors_pushsubscription` WRITE;
/*!40000 ALTER TABLE `vendors_pushsubscription` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_pushsubscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_pushsubscription_tokens`
--

DROP TABLE IF EXISTS `vendors_pushsubscription_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_pushsubscription_tokens` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pushsubscription_id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_pushsubscription_pushsubscription_id_orde_7b93da7b_uniq` (`pushsubscription_id`,`order_id`),
  KEY `vendors_pushsubscrip_order_id_7fb17505_fk_vendors_o` (`order_id`),
  CONSTRAINT `vendors_pushsubscrip_order_id_7fb17505_fk_vendors_o` FOREIGN KEY (`order_id`) REFERENCES `vendors_order` (`id`),
  CONSTRAINT `vendors_pushsubscrip_pushsubscription_id_951d3ebe_fk_vendors_p` FOREIGN KEY (`pushsubscription_id`) REFERENCES `vendors_pushsubscription` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=777 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_pushsubscription_tokens`
--

LOCK TABLES `vendors_pushsubscription_tokens` WRITE;
/*!40000 ALTER TABLE `vendors_pushsubscription_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_pushsubscription_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_siteconfig`
--

DROP TABLE IF EXISTS `vendors_siteconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_siteconfig` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `maintenance_mode` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_siteconfig`
--

LOCK TABLES `vendors_siteconfig` WRITE;
/*!40000 ALTER TABLE `vendors_siteconfig` DISABLE KEYS */;
INSERT INTO `vendors_siteconfig` VALUES (1,0);
/*!40000 ALTER TABLE `vendors_siteconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_vendor`
--

DROP TABLE IF EXISTS `vendors_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_vendor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `vendor_id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `place_id` varchar(255) DEFAULT NULL,
  `location_id` varchar(20) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `admin_outlet_id` bigint(20) NOT NULL,
  `ads` longtext DEFAULT NULL,
  `menus` longtext DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `alias_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendor_id` (`vendor_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `vendors_vendor_admin_outlet_id_eb9358a8_fk_vendors_a` (`admin_outlet_id`),
  CONSTRAINT `vendors_vendor_admin_outlet_id_eb9358a8_fk_vendors_a` FOREIGN KEY (`admin_outlet_id`) REFERENCES `vendors_adminoutlet` (`id`),
  CONSTRAINT `vendors_vendor_user_id_14564ee2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_vendor`
--

LOCK TABLES `vendors_vendor` WRITE;
/*!40000 ALTER TABLE `vendors_vendor` DISABLE KEYS */;
INSERT INTO `vendors_vendor` VALUES (1,'Starbucks - Lulu Mall','Lulu Mall',101,'2025-04-03 06:02:13.084690','2025-04-25 04:15:44.778052','ChIJ7Z1P3Ga9BTsR6Nqfe3ZXbU0','2001','vendor_logos/starbucks-coffee.svg',1,'','[\"\"]',NULL,NULL),(2,'Starbucks - City Square','City Square',102,'2025-04-03 06:03:50.827327','2025-04-03 06:03:50.827422','ChIJzwS7H8YZ2jERiigCiU-kxNM','2002','vendor_logos/starbucks-coffee.svg',1,NULL,'[\"\"]',NULL,NULL),(3,'Starbucks - Downtown Plaza','Downtown Plaza',103,'2025-04-03 06:10:59.518230','2025-04-03 06:10:59.518321','ChIJLR2RyMAnPw0REHtPOYYMm28','2003','vendor_logos/starbucks-coffee.svg',1,NULL,'[\"\"]',NULL,NULL),(4,'McDonald\'s - Lulu Mall','Lulu Mall',104,'2025-04-03 06:12:50.364426','2025-04-03 06:15:53.963739','ChIJN5t6A6K9BTsRlIxCvYrkrRo','2001','vendor_logos/McDonalds.svg',2,NULL,'[\"\"]',NULL,NULL),(5,'McDonald\'s - Grand Avenue','Grand Avenue',105,'2025-04-03 06:18:48.194656','2025-04-03 06:18:48.194770','ChIJNypXm7Ayw4AROJrcpgYCzco','2004','vendor_logos/McDonalds.svg',2,NULL,'[\"\"]',NULL,NULL),(6,'McDonald\'s - High Street','High Street',106,'2025-04-03 06:20:10.779983','2025-04-03 06:20:10.780077','ChIJT4-4ZbWn2EcR98RcV15H7-o','2005','vendor_logos/McDonalds.svg',2,NULL,'[\"\"]',NULL,NULL),(7,'KFC - Lulu Mall','Lulu Mall',107,'2025-04-03 06:22:05.359258','2025-04-07 05:03:00.207342','ChIJT29gy4y9BTsRRD_ajliCYNM','2001','vendor_logos/KFC.svg',3,'[\"ads/KFCAD1.jpg\", \"ads/KFCAD2.jpg\", \"ads/KFCAD3.jpg\", \"ads/KFCAD1_MGYn8Lu.jpg\", \"ads/KFCAD2_hYSEopS.jpg\", \"ads/KFCAD3_Ln1Z6tr.jpg\"]','[\"menus/AZADMENU.jpg\"]',NULL,NULL),(8,'KFC - Mega Mall','Mega Mall',108,'2025-04-03 06:23:27.440112','2025-04-03 06:23:27.440202','ChIJRcIRNgA5sz4RXkiyECPA7H0','2006','vendor_logos/KFC.svg',3,NULL,'[\"\"]',NULL,NULL),(9,'KFC - Express Highway','Express Highway',109,'2025-04-03 06:25:05.877282','2025-04-03 06:25:05.877370','ChIJpW6eIBS55zsRj9MCAp4b1M0','2007','vendor_logos/KFC.svg',3,NULL,'[\"\"]',NULL,NULL),(10,'KFC - City Square','City Square',110,'2025-04-03 06:26:38.630736','2025-04-03 06:26:38.630833','ChIJNe5w8DEZ6zkR0tjRB5STmd8','2002','vendor_logos/KFC.svg',3,NULL,'[\"\"]',NULL,NULL),(11,'Burger King - Lulu Mall','Lulu Mall',111,'2025-04-03 06:28:40.827054','2025-04-08 09:54:02.355450','ChIJt1BlK0W9BTsRKqYV9WWqKX8','2001','vendor_logos/Burger_King.svg',4,'[\"ads/BURGERKINGAD3.jpg\", \"ads/BURGERKINGAD2.jpg\", \"ads/BURGERKINGAD1.jpg\", \"ads/BURGERKINGAD1_uwtAGv3.jpg\", \"ads/BURGERKINGAD3_RqWHelO.jpg\"]','[\"menus/BURGERKINGMENU1.jpg\", \"menus/BURGERKINGMENU1_cpweVOo.jpg\", \"menus/BURGERKINGMENU1_14splsn.jpg\"]',NULL,NULL),(12,'Domino\'s - Lulu Mall','Lulu Mall',114,'2025-04-03 06:30:08.699623','2025-04-03 06:30:08.699714','ChIJwa0Zhx-9BTsRyiGJTyLFVSI','2001','vendor_logos/Dominos.svg',5,NULL,'[\"\"]',NULL,NULL),(13,'Pizza Hut - Lulu Mall','Lulu Mall',117,'2025-04-03 06:30:57.259222','2025-04-03 06:30:57.259315','ChIJy7PdYaq9BTsRXTeH2sKRB7Y','2001','vendor_logos/Pizza_Hut.svg',6,NULL,'[\"\"]',NULL,NULL),(14,'Subway - Lulu Mall','Lulu Mall',120,'2025-04-03 06:31:55.984004','2025-04-07 05:12:26.147926','ChIJGwLidmO9BTsR5qbbpGVv2xg','2001','vendor_logos/Subway.svg',7,'[\"ads/SUBWAYAD1.jpg\", \"ads/SUBWAYAD2.jpg\", \"ads/SUBWAYAD3.jpg\"]','[\"menus/SUBWAYMENU1.jpeg\"]',NULL,NULL),(15,'Costa Coffee - Lulu Mall','Lulu Mall',123,'2025-04-03 06:32:40.798167','2025-04-03 06:32:40.798259','ChIJyzoSWj_lmzkRu3hf2hs2vzY','2001','vendor_logos/Costa_Coffee_.svg',8,NULL,'[\"\"]',NULL,NULL),(16,'AZAD','Kazhakkuttam',472435,'2025-05-22 12:20:53.484078','2025-05-22 12:20:53.484105','ChIJoXPUuqa7BTsRSSujVeNeaiE','KZ01','vendor_logos/azad.png',3,NULL,'[\"menus/AZADAD2_DHNFRB5.jpg\"]',NULL,NULL),(51,'Demo1','Kowdiar',519488,'2025-06-04 10:47:14.270065','2025-06-26 11:57:33.714445','ChIJQ94r10S-BTsRDtOmYzIplto','KW01','vendor_logos/SOFTLAND_LOGO.png',19,'[\"ads/SOFTLAND1.jpg\", \"ads/SOFTLAND2.jpg\", \"ads/SOFTLAND3.jpg\", \"ads/SOFTLAND4.jpg\",\"ads/SOFTLAND1.jpg\", \"ads/SOFTLAND2.jpg\", \"ads/SOFTLAND3.jpg\", \"ads/SOFTLAND4.jpg\"]','[\"menus/BURGERKINGMENU1.jpg\"]',NULL,'Demo1'),(63,'Demo2','Trivandrum',265344,'2025-06-09 10:41:38.801264','2025-06-18 07:18:47.983082','ChIJQ94r10S-BTsRDtOmYzIplto','VAZ01','vendor_logos/SOFTLAND_LOGO_C4bMVXY.png',19,'[\"ads/SUBWAYAD1.jpg\", \"ads/SUBWAYAD2.jpg\", \"ads/SUBWAYAD3.jpg\"]','[\"menus/SUBWAYMENU1.jpeg\"]',NULL,'Demo2');
/*!40000 ALTER TABLE `vendors_vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_vendoradvertisement`
--

DROP TABLE IF EXISTS `vendors_vendoradvertisement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_vendoradvertisement` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_vendoradvert_vendor_id_59e5de59_fk_vendors_v` (`vendor_id`),
  CONSTRAINT `vendors_vendoradvert_vendor_id_59e5de59_fk_vendors_v` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_vendoradvertisement`
--

LOCK TABLES `vendors_vendoradvertisement` WRITE;
/*!40000 ALTER TABLE `vendors_vendoradvertisement` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_vendoradvertisement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_vendormenu`
--

DROP TABLE IF EXISTS `vendors_vendormenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_vendormenu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `vendor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_vendormenu_vendor_id_5397a062_fk_vendors_vendor_id` (`vendor_id`),
  CONSTRAINT `vendors_vendormenu_vendor_id_5397a062_fk_vendors_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors_vendor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_vendormenu`
--

LOCK TABLES `vendors_vendormenu` WRITE;
/*!40000 ALTER TABLE `vendors_vendormenu` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_vendormenu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webpush_group`
--

DROP TABLE IF EXISTS `webpush_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `webpush_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webpush_group`
--

LOCK TABLES `webpush_group` WRITE;
/*!40000 ALTER TABLE `webpush_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `webpush_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webpush_pushinformation`
--

DROP TABLE IF EXISTS `webpush_pushinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `webpush_pushinformation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `subscription_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `webpush_pushinformation_user_id_5e083b7f_fk_auth_user_id` (`user_id`),
  KEY `webpush_pushinformation_group_id_262dcc9a_fk` (`group_id`),
  KEY `webpush_pushinformation_subscription_id_7989aa34_fk` (`subscription_id`),
  CONSTRAINT `webpush_pushinformation_group_id_262dcc9a_fk` FOREIGN KEY (`group_id`) REFERENCES `webpush_group` (`id`),
  CONSTRAINT `webpush_pushinformation_subscription_id_7989aa34_fk` FOREIGN KEY (`subscription_id`) REFERENCES `webpush_subscriptioninfo` (`id`),
  CONSTRAINT `webpush_pushinformation_user_id_5e083b7f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webpush_pushinformation`
--

LOCK TABLES `webpush_pushinformation` WRITE;
/*!40000 ALTER TABLE `webpush_pushinformation` DISABLE KEYS */;
/*!40000 ALTER TABLE `webpush_pushinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webpush_subscriptioninfo`
--

DROP TABLE IF EXISTS `webpush_subscriptioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `webpush_subscriptioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `browser` varchar(100) NOT NULL,
  `endpoint` varchar(500) NOT NULL,
  `auth` varchar(100) NOT NULL,
  `p256dh` varchar(100) NOT NULL,
  `user_agent` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webpush_subscriptioninfo`
--

LOCK TABLES `webpush_subscriptioninfo` WRITE;
/*!40000 ALTER TABLE `webpush_subscriptioninfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `webpush_subscriptioninfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-02  9:40:35
