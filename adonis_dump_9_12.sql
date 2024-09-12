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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('014457e05b73');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `logs` VALUES ('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','JUMPING','did skips for 1hours','2024-09-08 23:12:49',10,'Manual','Completed','Private',NULL,'0af94b14-60ca-4945-b658-3414939f1a50','2024-09-08 20:12:50','2024-09-08 20:12:50'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','JUMPING','did skips for 1hours','2024-09-08 23:15:23',10,'Manual','Completed','Private',NULL,'412d8f0e-0785-4bb0-9b8a-6ee0060e2088','2024-09-08 20:15:23','2024-09-08 20:15:23'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','JUMPING','did skips for 1hours','2024-09-08 23:19:43',10,'Manual','Completed','Private',NULL,'65abca60-d744-4ca3-ac50-ba7308d38808','2024-09-08 20:19:44','2024-09-08 20:19:44'),('6e284691-9d69-48e6-9257-6b2af83b1b13','meditation','pre sleep meditation','asdas','2024-09-09 02:44:04',5,'Manual','Completed','Private',NULL,'6bcead72-2627-482c-800f-6cf9b76d21cc','2024-09-08 23:44:05','2024-09-08 23:44:05'),('6e284691-9d69-48e6-9257-6b2af83b1b13','meditation','body scan meditation','sat down for meditation in the afternoon','2024-09-09 02:32:22',5,'Manual','Completed','Private',NULL,'71523d23-1196-4268-8dec-7d491623ef5a','2024-09-08 23:32:23','2024-09-08 23:32:23'),('af27c778-964d-4491-8bd3-6a9ed15512ec','exercise','123','','2024-09-12 08:30:47',10,'Manual','Completed','Private',NULL,'771051f4-7a84-4aa7-b203-cd0c1a2c16fe','2024-09-12 05:30:47','2024-09-12 07:28:41'),('af27c778-964d-4491-8bd3-6a9ed15512ec','meditation','relaxed','deep scan for 20 min','2024-09-11 22:04:31',5,'Manual','Completed','Private',NULL,'8c2d3ce3-6efa-433f-8597-efe1d77642d6','2024-09-11 19:04:31','2024-09-12 05:15:06'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','JUMPING','did skips for 1hours','2024-09-08 23:18:53',10,'Manual','Completed','Private',NULL,'917cda0d-baca-46dd-8ceb-a6b2cd8b9347','2024-09-08 20:18:53','2024-09-08 20:18:53'),('6e284691-9d69-48e6-9257-6b2af83b1b13','meditation','body scan meditation','sat down for meditation in the afternoon','2024-09-08 23:21:04',5,'Manual','Completed','Private',NULL,'9516ceb8-c7f0-4264-8d5e-8a2598bc971b','2024-09-08 20:21:05','2024-09-08 20:21:05'),('af27c778-964d-4491-8bd3-6a9ed15512ec','health','drinking','drank 500ml of water','2024-09-12 08:35:40',0,'Manual','Completed','Private',NULL,'9c12396d-66f4-40e9-8040-7484aa176641','2024-09-12 05:35:40','2024-09-12 05:35:40'),('af27c778-964d-4491-8bd3-6a9ed15512ec','exercise','Deep Breathing','morning Breath work to jumpstart the day','2024-09-12 08:23:55',10,'Manual','Completed','Private',NULL,'affa1c33-48b1-4b48-943b-781e0be91250','2024-09-12 05:23:56','2024-09-12 07:09:03'),('af27c778-964d-4491-8bd3-6a9ed15512ec','learning','Aphorisms','i read unconventional aphorisms from precrustes','2024-09-12 08:21:00',0,'Manual','Completed','Private',NULL,'b46f129d-4b04-4098-b541-5980d4394f06','2024-09-12 05:21:01','2024-09-12 05:21:01'),('6e284691-9d69-48e6-9257-6b2af83b1b13','Sports','Running',NULL,'2024-09-08 22:11:36',0,'Manual','Completed','Private',NULL,'bb1f1d6c-f834-442a-909f-8bdf3a6f24e3','2024-09-08 19:11:36','2024-09-08 19:11:36'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','JUMPING','did skips for 1hours','2024-09-08 23:17:45',10,'Manual','Completed','Private',NULL,'bca1fc17-0de4-4d95-8e11-d529756e27cc','2024-09-08 20:17:46','2024-09-08 20:17:46'),('6e284691-9d69-48e6-9257-6b2af83b1b13','Sports','PushUps','I did 10 Push ups','2024-09-08 22:22:24',0,'Manual','Completed','Private',NULL,'cc01843e-93f5-427a-9145-412470523dc9','2024-09-08 19:22:24','2024-09-08 19:22:24'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','Workout','did a morning workout','2024-09-10 10:10:36',10,'Manual','Completed','Private',NULL,'d9e1989e-dc4b-4a80-8a52-ce544ab81158','2024-09-10 07:10:37','2024-09-10 07:10:37'),('6e284691-9d69-48e6-9257-6b2af83b1b13','Sports','Squats','I did 10 Squats','2024-09-08 22:23:42',10,'Manual','Completed','Private',NULL,'daa35a8d-2945-409c-877f-fb7113e91f9e','2024-09-08 19:23:43','2024-09-08 19:23:43'),('af27c778-964d-4491-8bd3-6a9ed15512ec','exercise','relaxed','','2024-09-12 08:32:29',10,'Manual','Completed','Private',NULL,'e86810df-915d-4169-9f76-0558b2e89691','2024-09-12 05:32:29','2024-09-12 07:42:48'),('6e284691-9d69-48e6-9257-6b2af83b1b13','meditation','body scan meditation 50','sat down for meditation in the morning','2024-09-11 19:58:41',5,'Manual','Completed','Private',NULL,'ebaf2a3c-998c-40e5-b420-b880bb4eca2a','2024-09-11 16:58:41','2024-09-11 16:58:41'),('6e284691-9d69-48e6-9257-6b2af83b1b13','exercise','Workout','did a morning workout','2024-09-10 10:10:25',10,'Manual','Completed','Private',NULL,'f5ad2693-9ada-4914-88ee-1375adda97e8','2024-09-10 07:10:25','2024-09-10 07:10:25');
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
  `category` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES ('Athlete','Fitness enthusiast',1,'341c2b75-95cf-4b34-8355-7901cb839630','2024-09-12 11:13:09','2024-09-12 11:13:09','Exercise and Fitness'),('Life of the Party','Never a dull time around you!',1,'37dab18c-b16b-4a4c-9718-c3acb3212d39','2024-09-12 11:13:09','2024-09-12 11:13:09','Social Interaction'),('Gym Shark','Your body is your temple!',1,'3e5e1b59-2e11-4500-98e9-f7cba05fab19','2024-09-12 11:13:09','2024-09-12 11:13:09','Exercise and Fitness'),('Good Guy','Lover of books',1,'4c5077d6-6927-4489-8053-7083067634dc','2024-09-12 11:13:09','2024-09-12 11:13:09','Other'),('Social Butterfly','People are your power!',1,'53fca75b-3b6d-43ee-aed8-82f3df79f5b9','2024-09-12 11:13:09','2024-09-12 11:13:09','Social Interaction'),('Code Junkie','Eat.Sleep.Code.Repeat.',1,'7cac0543-3f17-46c3-b4ec-6e1b58c14026','2024-09-12 11:13:09','2024-09-12 11:13:09','Other'),('Introvert','Time alone is time well spent!',1,'844f8586-fa52-4d22-8965-2ac579bb4a17','2024-09-12 11:13:09','2024-09-12 11:13:09','Social Interaction'),('Sport King','Competition is your drug',1,'8d3fba2e-76c1-4582-bcc3-5f7d5f5d4c84','2024-09-12 11:13:09','2024-09-12 11:13:09','Exercise and Fitness'),('Programmer','Lover of books',1,'8f05ce33-76d0-408f-842e-8560689cf9cf','2024-09-12 11:13:09','2024-09-12 11:13:09','Learning and Education'),('Lover','Lover of books',1,'a19df727-c511-41da-bd36-48a84a16c4c5','2024-09-12 11:13:09','2024-09-12 11:13:09','Other'),('Bibliophile','Lover of books',1,'a34519e8-eef5-4e18-bc80-8430e9c6d2d3','2024-09-12 11:13:09','2024-09-12 11:13:09','Learning and Education'),('Health Freak','Passionate about healthy living',1,'b0ecf8e6-db9d-4ff2-84dd-4e144165c9bc','2024-09-12 11:13:09','2024-09-12 11:13:09','Exercise and Fitness'),('Teacher','Lover of books',1,'bdc34cbd-4e9c-4bbd-bbdc-63f364bb0d7c','2024-09-12 11:13:09','2024-09-12 11:13:09','Other'),('Scholar','Chasing that knowledge!',1,'d746cb8e-3e87-401d-9991-c622fa760687','2024-09-12 11:13:09','2024-09-12 11:13:09','Learning and Education'),('Night Owl','You live for the nightlife!',1,'d8633502-40bc-4dbf-83ce-e8d171ccb5e4','2024-09-12 11:13:09','2024-09-12 11:13:09','Social Interaction'),('Mediator','You bring people together!',1,'ee8e027b-6799-4a35-adf0-27fa4ea9e94a','2024-09-12 11:13:09','2024-09-12 11:13:09','Social Interaction'),('Body Builder','Live for the gains',1,'f5e14ac9-b0a8-4b2e-90be-03d3507150dd','2024-09-12 11:13:09','2024-09-12 11:13:09','Exercise and Fitness'),('Friend','Lover of books',1,'fb3b4844-ab24-4f83-90f0-bd0b2b125794','2024-09-12 11:13:09','2024-09-12 11:13:09','Other');
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
INSERT INTO `user_sessions` VALUES ('6e284691-9d69-48e6-9257-6b2af83b1b13','82eb2c72-a338-419f-a69a-2d4fac9e3117','0072fa0b-9b90-44fc-94ab-44b9f0faf82b','2024-09-08 23:55:02','2024-09-08 20:55:02'),('6e284691-9d69-48e6-9257-6b2af83b1b13','f44fff6e-a73f-494c-b2d3-de848284df1b','0e7f4490-01ba-480c-a752-6e654752f619','2024-09-10 10:48:34','2024-09-10 07:48:34'),('6e284691-9d69-48e6-9257-6b2af83b1b13','be640358-b39a-4f48-929b-cd7c62e5d8cb','108ba73c-45a5-4850-9b1d-aa3f806c7c2c','2024-09-11 11:06:19','2024-09-11 08:06:19'),('6e284691-9d69-48e6-9257-6b2af83b1b13','b6f4848d-7cbb-45cf-9e0d-327f8bd10edc','113da39e-05c3-4cdf-8eb6-c6dfa6e5c0c2','2024-09-09 01:38:52','2024-09-08 22:38:53'),('6e284691-9d69-48e6-9257-6b2af83b1b13','f58ad723-b481-4d3e-ac12-b43c620c4e9e','114fcef4-7ae1-44be-ad1a-8aa582ef40af','2024-09-08 20:27:34','2024-09-08 17:27:34'),('6e284691-9d69-48e6-9257-6b2af83b1b13','9d43dd4d-232b-4b91-9a31-fd11c849add4','116e5e0b-bb6b-4600-aeb9-baf28541295e','2024-09-08 12:23:18','2024-09-08 09:23:18'),('6e284691-9d69-48e6-9257-6b2af83b1b13','cad84bb7-daff-4bdc-9278-52170a2113e2','11c243d4-2ac5-43cb-a0d6-963f8217a341','2024-09-11 21:29:20','2024-09-11 18:29:20'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e4dcfcf7-e1af-4cb3-8c9a-40d6387a0709','13b81ee0-8c4e-4870-9b9d-ed3a3d5e2f79','2024-09-09 01:51:59','2024-09-08 22:51:59'),('6e284691-9d69-48e6-9257-6b2af83b1b13','103b26cc-44e8-43d3-add6-f306a8560b1b','1c219d77-f191-4be8-b2e2-66bee39b2f84','2024-09-10 10:12:00','2024-09-10 07:12:01'),('6e284691-9d69-48e6-9257-6b2af83b1b13','fc4c506e-fc2e-4bb8-add7-a71a2e47321c','1cdfa3d7-5b9f-46f4-a986-d8efb105598d','2024-09-10 10:12:48','2024-09-10 07:12:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','429a5d35-8541-40ee-80ed-28a269ded8f2','23b7a209-aebf-4243-9b52-3a986d00ac4e','2024-09-09 00:00:07','2024-09-08 21:00:08'),('6e284691-9d69-48e6-9257-6b2af83b1b13','b6d57fbd-bc87-41b5-9652-03d5fb30ac87','28028d18-a12d-4318-b5fd-ffddaa270c6e','2024-09-09 11:52:28','2024-09-09 08:52:28'),('6e284691-9d69-48e6-9257-6b2af83b1b13','214bb03a-c174-437a-91d0-0c4a62c70ce0','2802a250-6c0a-44a0-a32a-c6a93453898e','2024-09-10 09:12:02','2024-09-10 06:12:03'),('af27c778-964d-4491-8bd3-6a9ed15512ec','7b5650dd-b35b-4d16-b86e-17745a9306b0','2819ec79-62f4-41fb-8638-bf3144d0c31b','2024-09-11 22:11:02','2024-09-11 19:11:03'),('6e284691-9d69-48e6-9257-6b2af83b1b13','99d3f662-8f36-4e9b-a310-b5cbc0251a36','2abb3c70-5c8f-4c85-960e-4a7a7e969aec','2024-09-09 02:11:55','2024-09-08 23:11:56'),('6e284691-9d69-48e6-9257-6b2af83b1b13','b7784a01-bb6f-42b8-8fa0-3746ddd76abc','2adf4d92-7a98-41e3-91f4-da42921fb257','2024-09-08 20:18:46','2024-09-08 17:18:47'),('6e284691-9d69-48e6-9257-6b2af83b1b13','858e3953-af2f-4cbc-bc04-2969551b32c6','2cbcc9d4-e890-45f7-b82e-244104860a9a','2024-09-11 21:21:51','2024-09-11 18:21:51'),('6e284691-9d69-48e6-9257-6b2af83b1b13','03cc7837-296c-4e69-8ce6-65ccc64601cb','2d742837-e323-4a70-9e02-471814c727bd','2024-09-09 01:36:27','2024-09-08 22:36:27'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e4570d48-f350-4b06-8c1f-94bfd6bc2b8c','2f2fa565-f173-4860-be52-76cbeaf2482d','2024-09-09 02:07:01','2024-09-08 23:07:02'),('6e284691-9d69-48e6-9257-6b2af83b1b13','6c8817c3-e689-4b4d-8d41-e9e8e3e7421f','2f6973c5-4668-4aeb-8782-4a941030e83a','2024-09-09 01:59:42','2024-09-08 22:59:43'),('6e284691-9d69-48e6-9257-6b2af83b1b13','f5a9106e-cb2f-47a6-bc61-7584604715de','33d39d48-b68c-4289-ab14-1ad2d618e284','2024-09-09 01:13:47','2024-09-08 22:13:48'),('6e284691-9d69-48e6-9257-6b2af83b1b13','22e7aadd-9cbb-428b-a712-a88ef99457ef','38271f17-5f80-416f-8447-3a7f99d26d73','2024-09-11 11:11:49','2024-09-11 08:11:50'),('6e284691-9d69-48e6-9257-6b2af83b1b13','84e8ee40-b25c-47bc-a6cf-f1f5eefdf8d7','3f159a41-5808-4f26-9254-a4cf2268f817','2024-09-09 02:17:47','2024-09-08 23:17:47'),('af27c778-964d-4491-8bd3-6a9ed15512ec','dc7d754d-dd1a-4d19-9f57-1d578c61005d','3f470949-ad22-418c-9d3e-af2e0ff5e19d','2024-09-12 07:50:48','2024-09-12 04:50:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','412fe51f-f359-470f-8c4d-be1e5df9e0dd','48b60934-b777-44d2-90b4-3042b8f1039c','2024-09-08 12:24:35','2024-09-08 09:24:36'),('af27c778-964d-4491-8bd3-6a9ed15512ec','9cdb49ed-fa84-4557-96cf-61c4a319f7a2','4bff2456-d0bf-496f-8729-a300bd42348c','2024-09-12 09:50:27','2024-09-12 06:50:27'),('6e284691-9d69-48e6-9257-6b2af83b1b13','219999a3-8e06-42a5-940d-482ec857b18f','4eb03869-715e-4b3c-b6af-c9c8098b9030','2024-09-11 09:36:33','2024-09-11 06:36:34'),('6e284691-9d69-48e6-9257-6b2af83b1b13','f599b69e-e3c4-4e62-8dfc-9eee2a7f96f7','509fec96-09c8-4486-bad1-938dbb1567cd','2024-09-10 09:56:04','2024-09-10 06:56:05'),('6e284691-9d69-48e6-9257-6b2af83b1b13','4b3159d5-1b28-4ce5-9246-7ce461e20d5e','51f6615d-7b34-4e72-a1f1-5d45ca66ef9e','2024-09-08 12:50:24','2024-09-08 09:50:25'),('6e284691-9d69-48e6-9257-6b2af83b1b13','667d9291-7a3a-4b67-9f85-ac164b11fd8b','54802538-e300-45a1-8e2d-35bb6406f359','2024-09-09 00:01:03','2024-09-08 21:01:03'),('6e284691-9d69-48e6-9257-6b2af83b1b13','ca2d6b3d-7013-435d-840f-1f50644bf3f3','61b4dfda-f20f-467b-ae4b-c203a4fdb1bc','2024-09-09 02:22:38','2024-09-08 23:22:38'),('6e284691-9d69-48e6-9257-6b2af83b1b13','3f7ceef2-0597-45f3-b4a9-9d7abc903db9','64e209d2-a41c-4059-a528-1de7d864d877','2024-09-08 12:15:39','2024-09-08 09:15:39'),('6e284691-9d69-48e6-9257-6b2af83b1b13','65937d24-9c1c-4e9c-880d-eb0c85eecb08','65bc19e9-bfd5-4aff-b347-98b052766307','2024-09-08 20:51:58','2024-09-08 17:51:59'),('6e284691-9d69-48e6-9257-6b2af83b1b13','557abf71-471a-489d-89e0-57d4f3e4cb99','67ccc2dc-2162-474e-af5c-71ea91bc2fda','2024-09-11 11:10:04','2024-09-11 08:10:05'),('6e284691-9d69-48e6-9257-6b2af83b1b13','68dbf9a3-abcc-4a6e-acb2-4003148736ab','6b397125-3942-49c6-ab2f-fad7620ad67e','2024-09-11 21:39:06','2024-09-11 18:39:06'),('6e284691-9d69-48e6-9257-6b2af83b1b13','d4558648-9dc8-404a-95eb-54b4a16984bb','6b3f40fb-a506-42bd-9145-0048accb2ea5','2024-09-08 20:29:04','2024-09-08 17:29:05'),('6e284691-9d69-48e6-9257-6b2af83b1b13','66f8e5fc-3a67-4a4f-b664-66d368c50358','6c1dede4-0364-4f55-b799-0e49009b0446','2024-09-08 20:26:49','2024-09-08 17:26:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','8d74dae7-e407-4334-b755-3a59bfc34e14','6f70ce9e-68d8-40a2-9105-ba1a3703dc86','2024-09-09 01:13:40','2024-09-08 22:13:40'),('6e284691-9d69-48e6-9257-6b2af83b1b13','c4ce13d4-41df-428c-8574-3a59583ae9e0','7142c02d-c191-478a-aaa9-51b6e1a6a40a','2024-09-11 21:45:30','2024-09-11 18:45:30'),('6e284691-9d69-48e6-9257-6b2af83b1b13','b1429eac-181b-44a1-867e-7a068f7ceee7','73cf2dad-3787-4b49-971e-1d6550442e23','2024-09-09 02:15:00','2024-09-08 23:15:01'),('6e284691-9d69-48e6-9257-6b2af83b1b13','a0726a2f-8f87-472d-9d72-05b32280f43e','752a2e2c-2cdf-452c-8cde-e12562303f17','2024-09-10 10:08:51','2024-09-10 07:08:52'),('6e284691-9d69-48e6-9257-6b2af83b1b13','87af8ab3-a47f-4f49-a6a8-3c397e996aae','78c14efd-c1f5-4a45-8943-1fcf4b3dacb5','2024-09-08 12:10:37','2024-09-08 09:10:38'),('6e284691-9d69-48e6-9257-6b2af83b1b13','00a77714-5e89-4c9d-8803-bfa49a0df8f7','78e7b0dd-709e-4c67-bbed-895d20d5ddf2','2024-09-08 12:19:48','2024-09-08 09:19:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','61b35f5b-8e51-4df8-9b5a-ca6f8911547b','83ff700e-e8a6-42cc-bddd-521e4695f3dc','2024-09-11 21:38:24','2024-09-11 18:38:25'),('646ff1b6-f951-45d7-a0a5-6330f386db3d','9c2b7f6e-0f13-423f-82d1-5c22acaaafdb','848b87e0-f3ea-456a-9959-e51738e0de30','2024-09-11 10:24:22','2024-09-11 07:24:23'),('6e284691-9d69-48e6-9257-6b2af83b1b13','83ee8cdf-b3c6-44c9-923d-4b43eb4e7980','978d59b0-b50e-48b9-82c4-a4f7e6740024','2024-09-09 01:51:10','2024-09-08 22:51:10'),('6e284691-9d69-48e6-9257-6b2af83b1b13','dbff20eb-710a-4eb3-a7ee-83d586926f56','9794701d-a5fa-4952-be63-f13830146e9e','2024-09-11 11:38:05','2024-09-11 08:38:05'),('6e284691-9d69-48e6-9257-6b2af83b1b13','8309254d-6d85-4e6d-be34-5ec0ec921043','9939b8ab-7c78-44f7-9b30-5b830e251abb','2024-09-09 02:01:42','2024-09-08 23:01:42'),('6e284691-9d69-48e6-9257-6b2af83b1b13','31f98368-154a-4649-9d1f-2c8cbf36e179','9b062b85-dfd0-4703-8320-286b06965e55','2024-09-11 21:41:15','2024-09-11 18:41:16'),('6e284691-9d69-48e6-9257-6b2af83b1b13','d43c9dea-393c-4deb-950a-4f95cb828876','a2080a2d-718b-4234-b768-ba7e73c68bc9','2024-09-08 12:10:41','2024-09-08 09:10:42'),('6e284691-9d69-48e6-9257-6b2af83b1b13','748a4641-ee77-4997-9c4c-2927dd119c9c','aa68c290-5fe9-4bd0-904b-a47898b0e545','2024-09-10 09:40:41','2024-09-10 06:40:41'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e401ebfa-77f6-44ff-af23-f8b86dda169c','acd29db5-65d7-48d0-a7f6-3b76c52818d5','2024-09-08 12:09:48','2024-09-08 09:09:48'),('6e284691-9d69-48e6-9257-6b2af83b1b13','0cecafce-a0e4-4d23-af7d-478f24ea3590','ae2d4799-0da5-4465-8bac-58d55db9318b','2024-09-09 01:12:04','2024-09-08 22:12:05'),('af27c778-964d-4491-8bd3-6a9ed15512ec','095f1c0c-d678-429d-8124-370881809194','b01dfb16-bafe-486a-aa58-9de3ffdf830a','2024-09-11 21:45:50','2024-09-11 18:45:50'),('6e284691-9d69-48e6-9257-6b2af83b1b13','c8068d72-1796-4ce1-afa2-6fa32aa8904e','b11c0a2f-f324-4a64-aadc-4c9822e3f15a','2024-09-11 21:32:02','2024-09-11 18:32:02'),('6e284691-9d69-48e6-9257-6b2af83b1b13','cf0b600e-3c31-4f2b-9b6a-e642607e88db','b121d4c3-d8c6-4674-9ad2-56749f9bd729','2024-09-09 01:24:43','2024-09-08 22:24:44'),('6e284691-9d69-48e6-9257-6b2af83b1b13','d4f7ae63-2eb5-4331-a9da-d30e71bbdad5','b3830ff0-939b-45ba-bc5e-8394424ea20f','2024-09-09 01:51:43','2024-09-08 22:51:44'),('6e284691-9d69-48e6-9257-6b2af83b1b13','cf867f77-8d87-4f62-a578-b39e663e9963','b4d0c2c1-30f2-4277-ae21-111407e58c60','2024-09-08 12:27:22','2024-09-08 09:27:23'),('6e284691-9d69-48e6-9257-6b2af83b1b13','d4a2de5f-4c51-4445-9845-9dc059e1a3f8','b5af2f34-5515-4642-8217-b94901a7fe3f','2024-09-09 01:17:07','2024-09-08 22:17:07'),('6e284691-9d69-48e6-9257-6b2af83b1b13','8fde941b-d282-43ae-9789-b9726f6f33da','b6e69cb1-caf0-48ca-a888-db2626501a33','2024-09-08 20:50:48','2024-09-08 17:50:49'),('6e284691-9d69-48e6-9257-6b2af83b1b13','0dcef70c-c75b-4ba2-9381-26354ac71b89','b7526fa8-0c49-4a6a-964e-a6a445b4d5fa','2024-09-09 01:29:04','2024-09-08 22:29:04'),('6e284691-9d69-48e6-9257-6b2af83b1b13','65babd73-26e8-4c42-91e8-e16841546489','b8620376-8aa4-4a48-a3ce-533231a4d3dd','2024-09-09 01:38:35','2024-09-08 22:38:36'),('6e284691-9d69-48e6-9257-6b2af83b1b13','74a10059-7075-468c-817c-56977248bdb0','baf93b66-3734-4b78-ab0a-b02bf84c257b','2024-09-09 02:03:11','2024-09-08 23:03:11'),('6e284691-9d69-48e6-9257-6b2af83b1b13','8adda9c1-ac60-4719-add3-4d2423b41722','c4bfb628-8158-4b50-a984-613a2e240e0c','2024-09-09 11:30:22','2024-09-09 08:30:23'),('5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','b3286077-c44a-49d4-ba1d-591f235d9470','c5318d95-893c-4a57-b417-2216930caeb3','2024-09-07 15:50:40','2024-09-07 12:50:40'),('6e284691-9d69-48e6-9257-6b2af83b1b13','707e4506-ed3d-4b7e-994a-ad277a4c114d','c655e317-4b65-437a-a1af-ab496c16d298','2024-09-08 21:08:30','2024-09-08 18:08:31'),('6e284691-9d69-48e6-9257-6b2af83b1b13','8cc4d5bc-15d4-424f-8f6e-d67b27dddf09','c8384c2f-03d5-4b02-b5da-2d3655895c59','2024-09-08 20:42:12','2024-09-08 17:42:12'),('ed6651b7-ccc5-4a4a-a7ec-0d2824dba905','40ff24af-a526-4e7f-91bc-0847c6a0fa3f','cca21287-575c-4d40-ad8c-b1e2ae510108','2024-09-08 13:48:46','2024-09-08 10:48:46'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e7f4fc5a-31c3-4b37-b866-471d175fa511','cd6fc268-6c5e-46e5-9f93-cd760bebfe0d','2024-09-11 21:34:07','2024-09-11 18:34:08'),('6e284691-9d69-48e6-9257-6b2af83b1b13','cd1a406a-db73-46a8-b755-9bc09496dc2f','cfd9436c-45a5-439c-84c9-2aea48697889','2024-09-11 11:38:39','2024-09-11 08:38:39'),('6e284691-9d69-48e6-9257-6b2af83b1b13','61543c17-927f-4211-b50b-24ce24f516ba','d2c8e7c5-d907-4b83-8254-0d49ee372873','2024-09-09 00:01:55','2024-09-08 21:01:56'),('6e284691-9d69-48e6-9257-6b2af83b1b13','6fe88cf2-e0fc-4884-b3d5-537c6dd946f4','dc95b82e-7b73-48f4-b5c2-99078b1f1029','2024-09-08 12:20:55','2024-09-08 09:20:56'),('6e284691-9d69-48e6-9257-6b2af83b1b13','6a9f1180-8304-41ff-90b7-da68f3faebdf','df0892fd-7f4c-4d1a-b6d1-87cabf95792a','2024-09-08 12:13:08','2024-09-08 09:13:09'),('6e284691-9d69-48e6-9257-6b2af83b1b13','601920de-25e9-4980-bed6-2e894c5ebc82','e07a052e-f00f-4de8-8336-0107b738e12b','2024-09-10 09:54:27','2024-09-10 06:54:28'),('6e284691-9d69-48e6-9257-6b2af83b1b13','10919800-e1e1-4e45-a46d-573b2bf619ba','e2b20f07-bfa0-4ae6-b181-34a66c4e155d','2024-09-09 02:08:00','2024-09-08 23:08:01'),('af27c778-964d-4491-8bd3-6a9ed15512ec','d5e1b193-1b3f-4cf5-8295-8e9b3b03b355','e704b67c-5400-4d92-9127-18d4c621f2ad','2024-09-12 07:51:35','2024-09-12 04:51:35'),('6e284691-9d69-48e6-9257-6b2af83b1b13','adac3ae3-e2f3-459d-874e-c2271ddc1bda','ec97f91f-c54d-4322-a012-ea18183a6842','2024-09-08 20:24:33','2024-09-08 17:24:33'),('6e284691-9d69-48e6-9257-6b2af83b1b13','a07a52cd-1cbd-4b85-81a9-0addfc98fe1d','edb0eefa-a8e2-49a9-a153-3040038fa7d0','2024-09-09 02:04:46','2024-09-08 23:04:46'),('6e284691-9d69-48e6-9257-6b2af83b1b13','0c0473ba-5f21-4320-8045-4f9fc4c6e65b','f2c8a40d-ce93-4cb3-9a84-8a7195ba3f82','2024-09-11 19:35:12','2024-09-11 16:35:12'),('d0c2a66e-1647-4788-897c-2893c39b7e91','13a730c0-fe4c-4d76-bd40-84dfc89a4a79','f4617d85-0f0d-4da3-80f4-a3a25d59d5ea','2024-09-08 10:51:20','2024-09-08 07:51:21'),('6e284691-9d69-48e6-9257-6b2af83b1b13','46ebdc2b-ff65-4b9c-a88e-cc0b4b41b527','f5f00867-d14f-49cd-8c11-0cb1f039a77a','2024-09-08 20:43:45','2024-09-08 17:43:46'),('6e284691-9d69-48e6-9257-6b2af83b1b13','330151a7-8ef3-44fd-87f1-677109591007','fa211414-90d5-453f-9873-66cc12b34b14','2024-09-08 11:43:38','2024-09-08 08:43:38'),('6e284691-9d69-48e6-9257-6b2af83b1b13','e70d5e4d-2e5c-4991-81e0-fe8d23bac651','fd7ca862-22f9-4b60-8dec-6ac28b101ac4','2024-09-08 12:50:38','2024-09-08 09:50:39');
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
  `id` varchar(36) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
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
  `age` int DEFAULT NULL,
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
INSERT INTO `users` VALUES ('testing3@gmail.com','testing3@gmail.com','JDJiJDEyJHpzcFJ4ekJpOHRienVNajlkM21VZnVyTnZHU1l6SUxPcXRrdTA5eDA0M1hGZ3hPUVZ6WDVp',NULL,NULL,'testing3@gmail.com','testing3@gmail.com',NULL,NULL,0,'2024-09-07 15:29:24',NULL,'4a7d884e-7601-4034-ae1f-23fe50f7122c','2024-09-07 12:29:24','2024-09-07 12:29:24',NULL),('testing7@gmail.com','testing7@gmail.com','JDJiJDEyJEJibXBvMWt4bVJZQlpNV2RsLnZqbi5KMjBwb0RCVDVacnlXWFRPSkFCU3R2Y2hIQkp6TzdX',NULL,NULL,'testing7@gmail.com','testing7@gmail.com',NULL,NULL,0,'2024-09-07 15:47:50',NULL,'4fcfeef4-0c4a-498a-8936-4d7a61864f3d','2024-09-07 12:47:50','2024-09-07 12:47:50',NULL),('testing2@gmail.com','testing2@gmail.com','JDJiJDEyJGVCcS5Deko1NVdYdnpBOUZxcVVYNGVGaGRPVzhkdzBCVzRGRmdHY1N1a3JxcjRpZzVkV1Vx',NULL,NULL,'testing2@gmail.com','testing2@gmail.com',NULL,NULL,0,'2024-09-07 15:26:44',NULL,'56bd2f1a-b33b-4fdc-8c48-9c27ae5bed9b','2024-09-07 12:26:45','2024-09-07 12:26:45',NULL),('testing9@gmail.com','testing9@gmail.com','JDJiJDEyJEgwR0h2czhKTEtHYjhzc1hCbXZSRHVUYllZSTFTLk9Tcng5UVdjOExneTJOZ3RoeFMua2d5',NULL,NULL,'testing9@gmail.com','testing9@gmail.com',NULL,NULL,0,'2024-09-07 15:50:40',NULL,'5e4e786f-e38d-49d3-99fd-7fd466d0cd2a','2024-09-07 12:50:40','2024-09-07 12:50:40',NULL),('scottshadow56@gmail.com','Scott_Admin','JDJiJDEyJHR6Nmd5bHBiYVBxMEZWU1RWejhKbS4zRkFIR09CN2MvR3JlM3hiY0w0TEkzenlxTXdiTi9H',NULL,NULL,'Scott','Dev',NULL,NULL,0,'2024-09-11 10:24:22',NULL,'646ff1b6-f951-45d7-a0a5-6330f386db3d','2024-09-11 07:24:23','2024-09-11 07:24:23',0),('testing@gmail.com','New_Me','JDJiJDEyJFBvL05ydlpZb1pDcjlPTUtDR0ZYbE9pd211Uk5ja09ycUxqZ1dJSDVRSzR1UUUuWFVsbnJx',NULL,NULL,'DEV','ACCOUNT',NULL,'Like to sleep',770,'2024-09-07 15:21:29',NULL,'6e284691-9d69-48e6-9257-6b2af83b1b13','2024-09-07 12:21:29','2024-09-12 07:42:14',NULL),('testing1000@gmail.com','testing1000@gmail.com','JDJiJDEyJHRWdDV1UlJNaUJod1BvVnhyZjdvMC5kLlNuQWlFWlFwUEhCSEsxenE0UG56YXY4amVSOTYu',NULL,NULL,'Scott','RUDASESWA',NULL,NULL,1950,'2024-09-11 21:45:50',NULL,'af27c778-964d-4491-8bd3-6a9ed15512ec','2024-09-11 18:45:50','2024-09-12 07:42:15',0),('testing4@gmail.com','testing4@gmail.com','JDJiJDEyJFBXZm55ZHdpQWRvLlZzaS9GMnU0M2ViUlNLWDRXZWhsVk1ESEViYzNXVDhUUURHTFg0cmFT',NULL,NULL,'testing4@gmail.com','testing4@gmail.com',NULL,NULL,0,'2024-09-07 15:32:06',NULL,'c57e8224-1b45-4ae7-aa2c-63e42bf33537','2024-09-07 12:32:06','2024-09-07 12:32:06',NULL),('testing10@gmail.com','testing10@gmail.com','JDJiJDEyJFljQjNIM1k3a29nVFlzaFB3WFZyVS5yOVlVUW8waWFsNFhFcU51SnFUVDk0ZUViaWdlc1FH',NULL,NULL,'testing10@gmail.com','testing10@gmail.com',NULL,NULL,0,'2024-09-07 15:53:41',NULL,'cc2ed518-a3dd-4ece-b035-b96b72a35acd','2024-09-07 12:53:41','2024-09-07 12:53:41',NULL),('testing13@gmail.com','testing13@gmail.com','JDJiJDEyJE5vU2ljUHE3QmhQUkJBY3V4Ty5TZGVzeW83dnhibVlYSWlneTBuRjRxemUuSjFneklJRk5D',NULL,NULL,'testing13@gmail.com','testing13@gmail.com',NULL,NULL,0,'2024-09-08 10:51:20',NULL,'d0c2a66e-1647-4788-897c-2893c39b7e91','2024-09-08 07:51:21','2024-09-08 07:51:21',NULL),('testing5@gmail.com','testing5@gmail.com','JDJiJDEyJDUxTmxkdncxdWdSSnNNNFJyM2lYYi5yOUJCa1dBMHhzQVFNbWFFVEJPS05NYm5nMTJXeEhp',NULL,NULL,'testing5@gmail.com','testing5@gmail.com',NULL,NULL,0,'2024-09-07 15:34:04',NULL,'d27407a0-7b31-44bc-a5de-25a6b74ad0c3','2024-09-07 12:34:05','2024-09-07 12:34:05',NULL),('testing100@gmail.com','testing100@gmail.com','JDJiJDEyJDRnUHE0NnI5OGxFQnEzbksuZzZKaWV4UGFieWhMZ3R1RGZ0YmphRThjTi42SEk3MWdqQW15',NULL,NULL,'testing100@gmail.com','testing100@gmail.com',NULL,NULL,0,'2024-09-08 13:48:46',NULL,'ed6651b7-ccc5-4a4a-a7ec-0d2824dba905','2024-09-08 10:48:46','2024-09-08 10:48:46',NULL);
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

-- Dump completed on 2024-09-12 14:16:16
