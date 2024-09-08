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
INSERT INTO `user_sessions` VALUES ('6e284691-9d69-48e6-9257-6b2af83b1b13','9d43dd4d-232b-4b91-9a31-fd11c849add4','116e5e0b-bb6b-4600-aeb9-baf28541295e','2024-09-08 12:23:18','2024-09-08 09:23:18'),('6e284691-9d69-48e6-9257-6b2af83b1b13','412fe51f-f359-470f-8c4d-be1e5df9e0dd','48b60934-b777-44d2-90b4-3042b8f1039c','2024-09-08 12:24:35','2024-09-08 09:24:36'),('6e284691-9d69-48e6-9257-6b2af83b1b13','4b3159d5-1b28-4ce5-9246-7ce461e20d5e','51f6615d-7b34-4e72-a1f1-5d45ca66ef9e','2024-09-08 12:50:24','2024-09-08 09:50:25'),('6e284691-9d69-48e6-9257-6b2af83b1b13','3f7ceef2-0597-45f3-b4a9-9d7abc903db9','64e209d2-a41c-4059-a528-1de7d864d877','2024-09-08 12:15:39','2024-09-08 09:15:39'),('6e284691-9d69-48e6-9257-6b2af83b1b13','87af8ab3-a47f-4f49-a6a8-3c397e996aae','78c14efd-c1f5-4a45-8943-1fcf4b3dacb5','2024-09-08 12:10:37','2024-09-08 09:10:38'),('6e284691-9d69-48e6-9257-6b2af83b1b13','00a77714-5e89-4c9d-8803-bfa49a0df8f7','78e7b0dd-709e-4c67-bbed-895d20d5ddf2','2024-09-08 12:19:48','2024-09-08 09:19:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','d43c9dea-393c-4deb-950a-4f95cb828876','a2080a2d-718b-4234-b768-ba7e73c68bc9','2024-09-08 12:10:41','2024-09-08 09:10:42'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e401ebfa-77f6-44ff-af23-f8b86dda169c','acd29db5-65d7-48d0-a7f6-3b76c52818d5','2024-09-08 12:09:48','2024-09-08 09:09:48'),('6e284691-9d69-48e6-9257-6b2af83b1b13','cf867f77-8d87-4f62-a578-b39e663e9963','b4d0c2c1-30f2-4277-ae21-111407e58c60','2024-09-08 12:27:22','2024-09-08 09:27:23'),('5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','b3286077-c44a-49d4-ba1d-591f235d9470','c5318d95-893c-4a57-b417-2216930caeb3','2024-09-07 15:50:40','2024-09-07 12:50:40'),('ed6651b7-ccc5-4a4a-a7ec-0d2824dba905','40ff24af-a526-4e7f-91bc-0847c6a0fa3f','cca21287-575c-4d40-ad8c-b1e2ae510108','2024-09-08 13:48:46','2024-09-08 10:48:46'),('6e284691-9d69-48e6-9257-6b2af83b1b13','6fe88cf2-e0fc-4884-b3d5-537c6dd946f4','dc95b82e-7b73-48f4-b5c2-99078b1f1029','2024-09-08 12:20:55','2024-09-08 09:20:56'),('6e284691-9d69-48e6-9257-6b2af83b1b13','6a9f1180-8304-41ff-90b7-da68f3faebdf','df0892fd-7f4c-4d1a-b6d1-87cabf95792a','2024-09-08 12:13:08','2024-09-08 09:13:09'),('d0c2a66e-1647-4788-897c-2893c39b7e91','13a730c0-fe4c-4d76-bd40-84dfc89a4a79','f4617d85-0f0d-4da3-80f4-a3a25d59d5ea','2024-09-08 10:51:20','2024-09-08 07:51:21'),('6e284691-9d69-48e6-9257-6b2af83b1b13','330151a7-8ef3-44fd-87f1-677109591007','fa211414-90d5-453f-9873-66cc12b34b14','2024-09-08 11:43:38','2024-09-08 08:43:38'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e70d5e4d-2e5c-4991-81e0-fe8d23bac651','fd7ca862-22f9-4b60-8dec-6ac28b101ac4','2024-09-08 12:50:38','2024-09-08 09:50:39');
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
INSERT INTO `users` VALUES ('testing3@gmail.com','testing3@gmail.com','JDJiJDEyJHpzcFJ4ekJpOHRienVNajlkM21VZnVyTnZHU1l6SUxPcXRrdTA5eDA0M1hGZ3hPUVZ6WDVp',NULL,NULL,'testing3@gmail.com','testing3@gmail.com',NULL,NULL,0,'2024-09-07 15:29:24',NULL,'4a7d884e-7601-4034-ae1f-23fe50f7122c','2024-09-07 12:29:24','2024-09-07 12:29:24'),('testing7@gmail.com','testing7@gmail.com','JDJiJDEyJEJibXBvMWt4bVJZQlpNV2RsLnZqbi5KMjBwb0RCVDVacnlXWFRPSkFCU3R2Y2hIQkp6TzdX',NULL,NULL,'testing7@gmail.com','testing7@gmail.com',NULL,NULL,0,'2024-09-07 15:47:50',NULL,'4fcfeef4-0c4a-498a-8936-4d7a61864f3d','2024-09-07 12:47:50','2024-09-07 12:47:50'),('testing2@gmail.com','testing2@gmail.com','JDJiJDEyJGVCcS5Deko1NVdYdnpBOUZxcVVYNGVGaGRPVzhkdzBCVzRGRmdHY1N1a3JxcjRpZzVkV1Vx',NULL,NULL,'testing2@gmail.com','testing2@gmail.com',NULL,NULL,0,'2024-09-07 15:26:44',NULL,'56bd2f1a-b33b-4fdc-8c48-9c27ae5bed9b','2024-09-07 12:26:45','2024-09-07 12:26:45'),('testing9@gmail.com','testing9@gmail.com','JDJiJDEyJEgwR0h2czhKTEtHYjhzc1hCbXZSRHVUYllZSTFTLk9Tcng5UVdjOExneTJOZ3RoeFMua2d5',NULL,NULL,'testing9@gmail.com','testing9@gmail.com',NULL,NULL,0,'2024-09-07 15:50:40',NULL,'5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','2024-09-07 12:50:40','2024-09-07 12:50:40'),('testing@gmail.com','testing@gmail.com','JDJiJDEyJHl2cGhaMDZ5OXNSRzRsc0trVWlwMi42eEpqNDhxRW9kYTk0b3l4TEh0NlFHaVNzbjdqVjJH',NULL,NULL,'testing@gmail.com','testing@gmail.com',NULL,NULL,0,'2024-09-07 15:21:29',NULL,'6e284691-9d69-48e6-9257-6b2af83b1b13','2024-09-07 12:21:29','2024-09-07 12:21:29'),('testing4@gmail.com','testing4@gmail.com','JDJiJDEyJFBXZm55ZHdpQWRvLlZzaS9GMnU0M2ViUlNLWDRXZWhsVk1ESEViYzNXVDhUUURHTFg0cmFT',NULL,NULL,'testing4@gmail.com','testing4@gmail.com',NULL,NULL,0,'2024-09-07 15:32:06',NULL,'c57e8224-1b45-4ae7-aa2c-63e42bf33537','2024-09-07 12:32:06','2024-09-07 12:32:06'),('testing10@gmail.com','testing10@gmail.com','JDJiJDEyJFljQjNIM1k3a29nVFlzaFB3WFZyVS5yOVlVUW8waWFsNFhFcU51SnFUVDk0ZUViaWdlc1FH',NULL,NULL,'testing10@gmail.com','testing10@gmail.com',NULL,NULL,0,'2024-09-07 15:53:41',NULL,'cc2ed518-a3dd-4ece-b035-b96b72a35acd','2024-09-07 12:53:41','2024-09-07 12:53:41'),('testing13@gmail.com','testing13@gmail.com','JDJiJDEyJE5vU2ljUHE3QmhQUkJBY3V4Ty5TZGVzeW83dnhibVlYSWlneTBuRjRxemUuSjFneklJRk5D',NULL,NULL,'testing13@gmail.com','testing13@gmail.com',NULL,NULL,0,'2024-09-08 10:51:20',NULL,'d0c2a66e-1647-4788-897c-2893c39b7e91','2024-09-08 07:51:21','2024-09-08 07:51:21'),('testing5@gmail.com','testing5@gmail.com','JDJiJDEyJDUxTmxkdncxdWdSSnNNNFJyM2lYYi5yOUJCa1dBMHhzQVFNbWFFVEJPS05NYm5nMTJXeEhp',NULL,NULL,'testing5@gmail.com','testing5@gmail.com',NULL,NULL,0,'2024-09-07 15:34:04',NULL,'d27407a0-7b31-44bc-a5de-25a6b74ad0c3','2024-09-07 12:34:05','2024-09-07 12:34:05'),('testing100@gmail.com','testing100@gmail.com','JDJiJDEyJDRnUHE0NnI5OGxFQnEzbksuZzZKaWV4UGFieWhMZ3R1RGZ0YmphRThjTi42SEk3MWdqQW15',NULL,NULL,'testing100@gmail.com','testing100@gmail.com',NULL,NULL,0,'2024-09-08 13:48:46',NULL,'ed6651b7-ccc5-4a4a-a7ec-0d2824dba905','2024-09-08 10:48:46','2024-09-08 10:48:46');
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

-- Dump completed on 2024-09-08 14:06:50
