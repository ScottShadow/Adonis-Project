-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: adonis_db
-- ------------------------------------------------------
-- Server version	8.0.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `log_tags`
--

DROP TABLE IF EXISTS `log_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_tags` (
  `tag_id` varchar(36) NOT NULL,
  `log_id` varchar(36) NOT NULL,
  PRIMARY KEY (`tag_id`,`log_id`),
  KEY `log_id` (`log_id`),
  CONSTRAINT `log_tags_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`),
  CONSTRAINT `log_tags_ibfk_2` FOREIGN KEY (`log_id`) REFERENCES `logs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tags`
--

LOCK TABLES `log_tags` WRITE;
/*!40000 ALTER TABLE `log_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `user_id` varchar(36) NOT NULL,
  `habit_type` varchar(50) NOT NULL,
  `habit_name` varchar(100) NOT NULL,
  `log_details` text,
  `timestamp` datetime NOT NULL,
  `xp` int DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `status` enum('Completed','Pending','Scheduled') DEFAULT NULL,
  `visibility` enum('Private','Friends','Clan','Public') NOT NULL,
  `shared_with` text,
  `id` varchar(36) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `name` varchar(250) NOT NULL,
  `category`  varchar(250) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `level` int DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `user_id` varchar(36) NOT NULL,
  `session_id` varchar(36) NOT NULL,
  `id` varchar(36) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
INSERT INTO `user_sessions` VALUES ('cc2ed518-a3dd-4ece-b035-b96b72a35acd','3c3e3dd6-5d40-4cca-b6f9-c34bbe4e4ebf','0ad6db5d-99df-4522-b7a4-31de66c5d8e0','2024-09-07 15:53:41','2024-09-07 12:53:41'),('5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','b3286077-c44a-49d4-ba1d-591f235d9470','c5318d95-893c-4a57-b417-2216930caeb3','2024-09-07 15:50:40','2024-09-07 12:50:40');
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tags`
--

DROP TABLE IF EXISTS `user_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tags` (
  `user_id` varchar(36) NOT NULL,
  `tag_id` varchar(36) NOT NULL,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `user_tags_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tags`
--

LOCK TABLES `user_tags` WRITE;
/*!40000 ALTER TABLE `user_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `email` varchar(250) NOT NULL,
  `username` varchar(250) NOT NULL,
  `hashed_password` varchar(250) NOT NULL,
  `session_id` varchar(250) DEFAULT NULL,
  `reset_token` varchar(250) DEFAULT NULL,
  `first_name` varchar(250) DEFAULT NULL,
  `last_name` varchar(250) DEFAULT NULL,
  `skills` varchar(250) DEFAULT NULL,
  `profile_info` varchar(500) DEFAULT NULL,
  `total_xp` int DEFAULT NULL,
  `account_created_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('testing3@gmail.com','testing3@gmail.com','JDJiJDEyJHpzcFJ4ekJpOHRienVNajlkM21VZnVyTnZHU1l6SUxPcXRrdTA5eDA0M1hGZ3hPUVZ6WDVp',NULL,NULL,'testing3@gmail.com','testing3@gmail.com',NULL,NULL,0,'2024-09-07 15:29:24',NULL,'4a7d884e-7601-4034-ae1f-23fe50f7122c','2024-09-07 12:29:24','2024-09-07 12:29:24'),('testing7@gmail.com','testing7@gmail.com','JDJiJDEyJEJibXBvMWt4bVJZQlpNV2RsLnZqbi5KMjBwb0RCVDVacnlXWFRPSkFCU3R2Y2hIQkp6TzdX',NULL,NULL,'testing7@gmail.com','testing7@gmail.com',NULL,NULL,0,'2024-09-07 15:47:50',NULL,'4fcfeef4-0c4a-498a-8936-4d7a61864f3d','2024-09-07 12:47:50','2024-09-07 12:47:50'),('testing2@gmail.com','testing2@gmail.com','JDJiJDEyJGVCcS5Deko1NVdYdnpBOUZxcVVYNGVGaGRPVzhkdzBCVzRGRmdHY1N1a3JxcjRpZzVkV1Vx',NULL,NULL,'testing2@gmail.com','testing2@gmail.com',NULL,NULL,0,'2024-09-07 15:26:44',NULL,'56bd2f1a-b33b-4fdc-8c48-9c27ae5bed9b','2024-09-07 12:26:45','2024-09-07 12:26:45'),('testing9@gmail.com','testing9@gmail.com','JDJiJDEyJEgwR0h2czhKTEtHYjhzc1hCbXZSRHVUYllZSTFTLk9Tcng5UVdjOExneTJOZ3RoeFMua2d5',NULL,NULL,'testing9@gmail.com','testing9@gmail.com',NULL,NULL,0,'2024-09-07 15:50:40',NULL,'5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','2024-09-07 12:50:40','2024-09-07 12:50:40'),('testing@gmail.com','testing@gmail.com','JDJiJDEyJHl2cGhaMDZ5OXNSRzRsc0trVWlwMi42eEpqNDhxRW9kYTk0b3l4TEh0NlFHaVNzbjdqVjJH',NULL,NULL,'testing@gmail.com','testing@gmail.com',NULL,NULL,0,'2024-09-07 15:21:29',NULL,'6e284691-9d69-48e6-9257-6b2af83b1b13','2024-09-07 12:21:29','2024-09-07 12:21:29'),('testing4@gmail.com','testing4@gmail.com','JDJiJDEyJFBXZm55ZHdpQWRvLlZzaS9GMnU0M2ViUlNLWDRXZWhsVk1ESEViYzNXVDhUUURHTFg0cmFT',NULL,NULL,'testing4@gmail.com','testing4@gmail.com',NULL,NULL,0,'2024-09-07 15:32:06',NULL,'c57e8224-1b45-4ae7-aa2c-63e42bf33537','2024-09-07 12:32:06','2024-09-07 12:32:06'),('testing10@gmail.com','testing10@gmail.com','JDJiJDEyJFljQjNIM1k3a29nVFlzaFB3WFZyVS5yOVlVUW8waWFsNFhFcU51SnFUVDk0ZUViaWdlc1FH',NULL,NULL,'testing10@gmail.com','testing10@gmail.com',NULL,NULL,0,'2024-09-07 15:53:41',NULL,'cc2ed518-a3dd-4ece-b035-b96b72a35acd','2024-09-07 12:53:41','2024-09-07 12:53:41'),('testing5@gmail.com','testing5@gmail.com','JDJiJDEyJDUxTmxkdncxdWdSSnNNNFJyM2lYYi5yOUJCa1dBMHhzQVFNbWFFVEJPS05NYm5nMTJXeEhp',NULL,NULL,'testing5@gmail.com','testing5@gmail.com',NULL,NULL,0,'2024-09-07 15:34:04',NULL,'d27407a0-7b31-44bc-a5de-25a6b74ad0c3','2024-09-07 12:34:05','2024-09-07 12:34:05');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-07 16:08:21
