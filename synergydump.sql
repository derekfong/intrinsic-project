-- MySQL dump 10.13  Distrib 5.1.61, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: synergydb
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.11.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Calendar_event`
--

DROP TABLE IF EXISTS `Calendar_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Calendar_event` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `lid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  `event_name` varchar(64) NOT NULL,
  `date` datetime NOT NULL,
  `location` varchar(64) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`eid`),
  KEY `Calendar_event_47b4da54` (`lid_id`),
  KEY `Calendar_event_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Calendar_event`
--

LOCK TABLES `Calendar_event` WRITE;
/*!40000 ALTER TABLE `Calendar_event` DISABLE KEYS */;
INSERT INTO `Calendar_event` VALUES (1,1,1,2,'Assignment 1','2012-04-04 00:00:00','','You will be creating a replacement to the AES encryption system. If it does not succeed you, you will automatically receive a failing grade in this course.'),(2,1,1,2,'Final','2012-04-16 12:00:00','',''),(3,1,1,2,'Assignment 2','2012-04-17 00:00:00','',''),(4,2,2,4,'Assignment 1','2012-04-24 00:00:00','','This is the first assignment of the semester.'),(6,3,2,NULL,'MCF Shift','2012-04-23 08:00:00','AQ3148','MCF Shift evening with people and others'),(7,1,1,2,'Midterm','2012-03-20 00:00:00','','Will cover chapters 1-9'),(8,1,1,2,'Midterm 1','2012-03-20 00:00:00','','Covers chapters 1-9'),(9,4,1,NULL,'Have fun','2012-04-19 00:00:00','Everywhere','It\'s going to be a blast!');
/*!40000 ALTER TABLE `Calendar_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Calendar_label`
--

DROP TABLE IF EXISTS `Calendar_label`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Calendar_label` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `color` varchar(32) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`lid`),
  KEY `Calendar_label_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Calendar_label`
--

LOCK TABLES `Calendar_label` WRITE;
/*!40000 ALTER TABLE `Calendar_label` DISABLE KEYS */;
INSERT INTO `Calendar_label` VALUES (1,'CMPT 404','Chocolate',1,2),(2,'CMPT 471','Cyan',2,4),(3,'Work','DarkBlue',2,NULL),(4,'Fun Stuff','Purple',1,NULL);
/*!40000 ALTER TABLE `Calendar_label` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Forum_messages`
--

DROP TABLE IF EXISTS `Forum_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Forum_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `user` varchar(100) NOT NULL,
  `creation_date` datetime NOT NULL,
  `message` longtext NOT NULL,
  `not_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Forum_messages_57732028` (`topic_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Forum_messages`
--

LOCK TABLES `Forum_messages` WRITE;
/*!40000 ALTER TABLE `Forum_messages` DISABLE KEYS */;
INSERT INTO `Forum_messages` VALUES (1,1,'kma50','2012-04-11 12:13:25','This is your instructor in this class, I wanted to let you all know that I look forward to a good semester.',1),(2,1,'kma50','2012-04-11 12:14:06','One more, thing. Good luck.',1),(3,1,'apike','2012-04-11 12:16:22','I look forward to it.',1),(4,2,'apike','2012-04-11 12:16:36','Just wanted to say hi!',1);
/*!40000 ALTER TABLE `Forum_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Forum_topics`
--

DROP TABLE IF EXISTS `Forum_topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Forum_topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_name` varchar(125) NOT NULL,
  `course_id` int(11) NOT NULL,
  `not_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Forum_topics_b7271b` (`course_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Forum_topics`
--

LOCK TABLES `Forum_topics` WRITE;
/*!40000 ALTER TABLE `Forum_topics` DISABLE KEYS */;
INSERT INTO `Forum_topics` VALUES (1,'Hi Everyone!',2,1),(2,'Hey all',2,1);
/*!40000 ALTER TABLE `Forum_topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gradebook_grade`
--

DROP TABLE IF EXISTS `Gradebook_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gradebook_grade` (
  `gid` int(11) NOT NULL AUTO_INCREMENT,
  `aid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `mark` decimal(10,2) NOT NULL,
  PRIMARY KEY (`gid`),
  KEY `Gradebook_grade_10ff6b97` (`aid_id`),
  KEY `Gradebook_grade_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gradebook_grade`
--

LOCK TABLES `Gradebook_grade` WRITE;
/*!40000 ALTER TABLE `Gradebook_grade` DISABLE KEYS */;
INSERT INTO `Gradebook_grade` VALUES (1,1,6,'85.00'),(2,1,9,'76.00'),(3,1,5,'91.00'),(4,1,4,'100.00'),(5,1,8,'97.00'),(6,1,7,'98.00'),(7,3,6,'0.00'),(8,3,9,'0.00'),(9,3,5,'0.00'),(10,3,4,'100.00'),(11,3,8,'100.00'),(12,3,7,'0.00'),(13,6,6,'85.00'),(14,6,9,'64.00'),(15,6,5,'69.00'),(16,6,4,'100.00'),(17,6,8,'87.00'),(18,6,7,'78.00');
/*!40000 ALTER TABLE `Gradebook_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gradebook_gradecomment`
--

DROP TABLE IF EXISTS `Gradebook_gradecomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gradebook_gradecomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gid_id` int(11) NOT NULL,
  `description` varchar(256) NOT NULL,
  `comment` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Gradebook_gradecomment_daae703` (`gid_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gradebook_gradecomment`
--

LOCK TABLES `Gradebook_gradecomment` WRITE;
/*!40000 ALTER TABLE `Gradebook_gradecomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Gradebook_gradecomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_activity`
--

DROP TABLE IF EXISTS `Instructor_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_activity` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `activity_name` varchar(256) NOT NULL,
  `out_of` decimal(5,2) NOT NULL,
  `worth` int(11) NOT NULL,
  `due_date` datetime NOT NULL,
  `submission_file_type` varchar(64) NOT NULL,
  `description` longtext NOT NULL,
  `description_doc` varchar(100) NOT NULL,
  `status` int(11) NOT NULL,
  `released` tinyint(1) NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `Instructor_activity_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_activity`
--

LOCK TABLES `Instructor_activity` WRITE;
/*!40000 ALTER TABLE `Instructor_activity` DISABLE KEYS */;
INSERT INTO `Instructor_activity` VALUES (1,2,'Assignment 1','100.00',10,'2012-04-04 00:00:00','No Submission','You will be creating a replacement to the AES encryption system. If it does not succeed you, you will automatically receive a failing grade in this course.','',2,1),(2,2,'Final','100.00',44,'2012-04-16 12:00:00','No Submission','','',0,0),(3,2,'Assignment 2','100.00',10,'2012-04-17 00:00:00','.pdf','','',0,0),(4,4,'Assignment 1','25.00',25,'2012-04-24 00:00:00','No Submission','This is the first assignment of the semester.','',0,0),(6,2,'Midterm 1','100.00',36,'2012-03-20 00:00:00','No Submission','Covers chapters 1-9','',0,0);
/*!40000 ALTER TABLE `Instructor_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_announcement`
--

DROP TABLE IF EXISTS `Instructor_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_announcement` (
  `anid` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `title` varchar(256) NOT NULL,
  `content` longtext NOT NULL,
  `date_posted` datetime NOT NULL,
  `send_email` tinyint(1) NOT NULL,
  `was_updated` tinyint(1) NOT NULL,
  `updated_by_id` int(11) NOT NULL,
  `updated_on` datetime NOT NULL,
  PRIMARY KEY (`anid`),
  KEY `Instructor_announcement_3f1da1a7` (`cid_id`),
  KEY `Instructor_announcement_2600da4b` (`uid_id`),
  KEY `Instructor_announcement_6f403c1` (`updated_by_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_announcement`
--

LOCK TABLES `Instructor_announcement` WRITE;
/*!40000 ALTER TABLE `Instructor_announcement` DISABLE KEYS */;
INSERT INTO `Instructor_announcement` VALUES (2,2,1,'Tomorrow\'s Lecture','Tomorrow\'s lecture will be on Quantum computing and will be completely optional. I hope to see you all there, with smiles on.','2012-04-09 23:23:43',0,0,1,'2012-04-09 23:23:43'),(3,2,1,'Grade released for Assignment 1','A new grade was released for Assignment 1. ','2012-04-09 23:24:48',0,1,1,'2012-04-11 11:36:10');
/*!40000 ALTER TABLE `Instructor_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_announceread`
--

DROP TABLE IF EXISTS `Instructor_announceread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_announceread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_announceread_622eaf66` (`anid_id`),
  KEY `Instructor_announceread_2600da4b` (`uid_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_announceread`
--

LOCK TABLES `Instructor_announceread` WRITE;
/*!40000 ALTER TABLE `Instructor_announceread` DISABLE KEYS */;
/*!40000 ALTER TABLE `Instructor_announceread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_coursecontent`
--

DROP TABLE IF EXISTS `Instructor_coursecontent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_coursecontent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `officeHrs` varchar(128) NOT NULL,
  `officeLocation` varchar(128) NOT NULL,
  `phoneNumber` varchar(12) NOT NULL,
  `TaOfficeLocation` varchar(128) NOT NULL,
  `TaOfficeHrs` varchar(128) NOT NULL,
  `lectTime` varchar(128) NOT NULL,
  `prereq` varchar(128) NOT NULL,
  `books` longtext NOT NULL,
  `topics` longtext NOT NULL,
  `markingScheme` longtext NOT NULL,
  `academicHonesty` longtext NOT NULL,
  `additionalInfo` longtext NOT NULL,
  `created_on` datetime NOT NULL,
  `was_updated` tinyint(1) NOT NULL,
  `updated_on` datetime NOT NULL,
  `file_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_coursecontent_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_coursecontent`
--

LOCK TABLES `Instructor_coursecontent` WRITE;
/*!40000 ALTER TABLE `Instructor_coursecontent` DISABLE KEYS */;
INSERT INTO `Instructor_coursecontent` VALUES (1,2,'Tuesday 12-2pm','AQ 3148.1','778-782-3230','TASC II 8012','Wednesday 10-12pm','MWF 11:30 - 12:20','MACM 201 and Algorithm knowledge','Discrete Mathematics and Combinators - R. Grimaldi, 2005\r\nData Networks and Communications - Berouz A. Ferouzan, 2006','Classic Cryptography\r\nPseudorandom Generators\r\nPublic Key Cryptography\r\nZero Knowledge proofs\r\nQuantum Cryptography','Quizzes - 24% (3 of them)\r\nHomeworks - 32% (4 of them)\r\nFinal - 44% ','Please be honest or you will be publicly shamed and possibly killed in a disturbing, gruesome death in front of all your peers with your pants possibly down.','None','2012-04-09 22:57:00',1,'2012-04-11 11:32:27','');
/*!40000 ALTER TABLE `Instructor_coursecontent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_greeting`
--

DROP TABLE IF EXISTS `Instructor_greeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_greeting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_greeting_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_greeting`
--

LOCK TABLES `Instructor_greeting` WRITE;
/*!40000 ALTER TABLE `Instructor_greeting` DISABLE KEYS */;
INSERT INTO `Instructor_greeting` VALUES (1,2,'I would like to welcome you all to CMPT 404, Cryptography and Protocols.  I look forward to this semester and I hope you all have fun and enjoy. Please enjoy all that life has to offer.  \r\n\r\nThank you,\r\n\r\nDr. Mann, PhD');
/*!40000 ALTER TABLE `Instructor_greeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_quiz`
--

DROP TABLE IF EXISTS `Instructor_quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_quiz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `student_attempts` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_quiz_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_quiz`
--

LOCK TABLES `Instructor_quiz` WRITE;
/*!40000 ALTER TABLE `Instructor_quiz` DISABLE KEYS */;
INSERT INTO `Instructor_quiz` VALUES (1,2,'Introduction','2012-04-10 00:21:00','2012-04-24 00:00:00',4);
/*!40000 ALTER TABLE `Instructor_quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_quizquestion`
--

DROP TABLE IF EXISTS `Instructor_quizquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_quizquestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qid_id` int(11) NOT NULL,
  `question` varchar(512) NOT NULL,
  `option1` varchar(512) NOT NULL,
  `option2` varchar(512) NOT NULL,
  `option3` varchar(512) NOT NULL,
  `option4` varchar(512) NOT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_quizquestion_317ef19` (`qid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_quizquestion`
--

LOCK TABLES `Instructor_quizquestion` WRITE;
/*!40000 ALTER TABLE `Instructor_quizquestion` DISABLE KEYS */;
INSERT INTO `Instructor_quizquestion` VALUES (1,1,'In asymmetric cryptography, how many keys are required for communication?','1','2','3','4',1),(2,1,'Private key must __________','Be distributed','Be shared with everyone','Remain secret','None of the above',2),(3,1,'Symmetric key encryption is ___________ than asymmetric key encryption','always faster ','of the same speed','slower','faster',3),(4,1,'_________ is a message digest algorithm','AES','DES','MD5','Django',2);
/*!40000 ALTER TABLE `Instructor_quizquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructor_slide`
--

DROP TABLE IF EXISTS `Instructor_slide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instructor_slide` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `uploaded_on` datetime NOT NULL,
  `file_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_slide_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructor_slide`
--

LOCK TABLES `Instructor_slide` WRITE;
/*!40000 ALTER TABLE `Instructor_slide` DISABLE KEYS */;
INSERT INTO `Instructor_slide` VALUES (1,2,'Lecture 1 - Introductions','2012-04-11 11:32:58','slides/2012/Spring/CMPT/404/D100/01_1.pdf'),(2,2,'Lecture 2 - Classical Cryptography','2012-04-09 23:04:05','slides/2012/Spring/CMPT/404/D100/02_1.pdf'),(3,2,'Lecture 3 - Statistical Security','2012-04-09 23:04:17','slides/2012/Spring/CMPT/404/D100/03.pdf'),(4,2,'Lecture 4 - Computational Security','2012-04-09 23:04:35','slides/2012/Spring/CMPT/404/D100/04.pdf'),(7,2,'Lecture 5 - Pseudorandom Generators','2012-04-11 11:33:49','slides/2012/Spring/CMPT/404/D100/05_2.pdf');
/*!40000 ALTER TABLE `Instructor_slide` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_classlist`
--

DROP TABLE IF EXISTS `Main_classlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_classlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` int(11) NOT NULL,
  `cid_id` int(11) NOT NULL,
  `is_instructor` tinyint(1) NOT NULL,
  `is_ta` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Main_classlist_2600da4b` (`uid_id`),
  KEY `Main_classlist_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_classlist`
--

LOCK TABLES `Main_classlist` WRITE;
/*!40000 ALTER TABLE `Main_classlist` DISABLE KEYS */;
INSERT INTO `Main_classlist` VALUES (1,4,1,1,0),(2,1,1,0,0),(3,2,1,0,0),(4,3,1,0,0),(5,10,4,0,0),(6,11,4,0,0),(7,12,4,0,0),(8,13,4,0,0),(9,14,4,0,0),(10,5,2,0,0),(11,6,2,0,0),(12,7,2,0,0),(13,8,2,0,0),(14,9,2,0,0),(15,1,2,1,0),(16,2,2,0,1),(17,1,4,0,1),(18,2,4,1,0),(19,4,3,0,0),(20,4,2,0,0);
/*!40000 ALTER TABLE `Main_classlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_course`
--

DROP TABLE IF EXISTS `Main_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(256) NOT NULL,
  `class_number` varchar(3) NOT NULL,
  `department` varchar(4) NOT NULL,
  `semester` varchar(16) NOT NULL,
  `year` int(11) NOT NULL,
  `section` varchar(4) NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_course`
--

LOCK TABLES `Main_course` WRITE;
/*!40000 ALTER TABLE `Main_course` DISABLE KEYS */;
INSERT INTO `Main_course` VALUES (1,'Web-Based Information Systems','470','CMPT','Spring',2012,'E100'),(2,'Cryptography and Protocols','404','CMPT','Spring',2012,'D100'),(3,'Poetry in the 1540 Computer Age','765','ENGL','Spring',2011,'D100'),(4,'Networking II','471','CMPT','Spring',2012,'D100');
/*!40000 ALTER TABLE `Main_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_setting`
--

DROP TABLE IF EXISTS `Main_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` int(11) NOT NULL,
  `email_announcement` tinyint(1) NOT NULL,
  `email_activity` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Main_setting_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_setting`
--

LOCK TABLES `Main_setting` WRITE;
/*!40000 ALTER TABLE `Main_setting` DISABLE KEYS */;
INSERT INTO `Main_setting` VALUES (8,4,0,0),(9,2,1,1),(10,1,1,1),(11,7,0,0);
/*!40000 ALTER TABLE `Main_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_uploadclasslist`
--

DROP TABLE IF EXISTS `Main_uploadclasslist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_uploadclasslist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `upload_date` datetime NOT NULL,
  `is_enrolled` tinyint(1) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Main_uploadclasslist_3f1da1a7` (`cid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_uploadclasslist`
--

LOCK TABLES `Main_uploadclasslist` WRITE;
/*!40000 ALTER TABLE `Main_uploadclasslist` DISABLE KEYS */;
INSERT INTO `Main_uploadclasslist` VALUES (1,2,'2012-04-09 22:47:55',1,'enrollment_lists/class_list_1.xls'),(2,4,'2012-04-09 22:47:55',1,'enrollment_lists/class_list_2.xls');
/*!40000 ALTER TABLE `Main_uploadclasslist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_uploaduserlist`
--

DROP TABLE IF EXISTS `Main_uploaduserlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_uploaduserlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(64) NOT NULL,
  `upload_date` datetime NOT NULL,
  `is_imported` tinyint(1) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_uploaduserlist`
--

LOCK TABLES `Main_uploaduserlist` WRITE;
/*!40000 ALTER TABLE `Main_uploaduserlist` DISABLE KEYS */;
INSERT INTO `Main_uploaduserlist` VALUES (1,'Master List','2012-04-09 22:18:39',1,'new_users/master_user_list.xls');
/*!40000 ALTER TABLE `Main_uploaduserlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Main_userprofile`
--

DROP TABLE IF EXISTS `Main_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Main_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `sfu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `sfu_id` (`sfu_id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Main_userprofile`
--

LOCK TABLES `Main_userprofile` WRITE;
/*!40000 ALTER TABLE `Main_userprofile` DISABLE KEYS */;
INSERT INTO `Main_userprofile` VALUES (1,1,556003392),(2,2,301068984),(3,3,301012345),(4,4,301098765),(5,5,111111111),(6,6,111111112),(7,7,111111113),(8,8,111111114),(9,9,111111115),(10,10,222222221),(11,11,222222222),(12,12,222222223),(13,13,222222224),(14,14,222222225),(15,15,333333331),(16,16,333333332),(17,17,333333333),(18,18,333333334),(19,19,333333335),(20,20,444444441),(21,21,444444442),(22,22,444444443),(23,23,444444444),(24,24,444444445),(25,25,555555551),(26,26,555555552),(27,27,555555553),(28,28,555555554),(29,29,555555555);
/*!40000 ALTER TABLE `Main_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student_quizattempt`
--

DROP TABLE IF EXISTS `Student_quizattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Student_quizattempt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `result` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Student_quizattempt_317ef19` (`qid_id`),
  KEY `Student_quizattempt_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student_quizattempt`
--

LOCK TABLES `Student_quizattempt` WRITE;
/*!40000 ALTER TABLE `Student_quizattempt` DISABLE KEYS */;
INSERT INTO `Student_quizattempt` VALUES (1,1,1,'2012-04-10 00:24:38',4),(2,1,2,'2012-04-10 00:25:03',0),(3,1,2,'2012-04-10 00:25:12',0),(4,1,2,'2012-04-10 00:25:18',0),(5,1,1,'2012-04-10 11:37:48',1),(6,1,1,'2012-04-10 11:39:58',0),(7,1,4,'2012-04-10 16:47:35',2),(8,1,1,'2012-04-11 12:12:30',2);
/*!40000 ALTER TABLE `Student_quizattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student_quizresult`
--

DROP TABLE IF EXISTS `Student_quizresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Student_quizresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attempt_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `guess` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Student_quizresult_72e81e20` (`attempt_id`),
  KEY `Student_quizresult_1f92e550` (`question_id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student_quizresult`
--

LOCK TABLES `Student_quizresult` WRITE;
/*!40000 ALTER TABLE `Student_quizresult` DISABLE KEYS */;
INSERT INTO `Student_quizresult` VALUES (1,1,1,1),(2,1,2,2),(3,1,3,3),(4,1,4,2),(5,2,1,0),(6,2,2,0),(7,2,3,0),(8,2,4,0),(9,3,1,0),(10,3,2,0),(11,3,3,0),(12,3,4,0),(13,4,1,0),(14,4,2,0),(15,4,3,0),(16,4,4,0),(17,5,1,3),(18,5,2,3),(19,5,3,3),(20,5,4,3),(21,6,1,3),(22,6,2,1),(23,6,3,0),(24,6,4,3),(25,7,1,1),(26,7,2,2),(27,7,3,2),(28,7,4,1),(29,8,1,2),(30,8,2,2),(31,8,3,2),(32,8,4,2);
/*!40000 ALTER TABLE `Student_quizresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student_submission`
--

DROP TABLE IF EXISTS `Student_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Student_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  `submit_date` datetime NOT NULL,
  `submit_number` int(11) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Student_submission_10ff6b97` (`aid_id`),
  KEY `Student_submission_2600da4b` (`uid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student_submission`
--

LOCK TABLES `Student_submission` WRITE;
/*!40000 ALTER TABLE `Student_submission` DISABLE KEYS */;
INSERT INTO `Student_submission` VALUES (1,3,2,'2012-04-09 23:38:54',1,'submissions/2012/Spring/CMPT/404/D100/Assignment 2/drf1/Hw.docx'),(2,3,2,'2012-04-10 00:14:02',2,'submissions/2012/Spring/CMPT/404/D100/Assignment 2/drf1/Hw_1.docx'),(3,3,5,'2012-04-10 00:55:47',1,'submissions/2012/Spring/CMPT/404/D100/Assignment 2/dnonis/Hw.docx'),(4,3,7,'2012-04-11 14:19:09',1,'submissions/2012/Spring/CMPT/404/D100/Assignment 2/hsedin/Assignment 2.pdf'),(5,3,7,'2012-04-11 14:19:51',2,'submissions/2012/Spring/CMPT/404/D100/Assignment 2/hsedin/HENRIK SEDIN.pdf');
/*!40000 ALTER TABLE `Student_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add label',9,'add_label'),(26,'Can change label',9,'change_label'),(27,'Can delete label',9,'delete_label'),(28,'Can add event',10,'add_event'),(29,'Can change event',10,'change_event'),(30,'Can delete event',10,'delete_event'),(31,'Can add grade',11,'add_grade'),(32,'Can change grade',11,'change_grade'),(33,'Can delete grade',11,'delete_grade'),(34,'Can add grade comment',12,'add_gradecomment'),(35,'Can change grade comment',12,'change_gradecomment'),(36,'Can delete grade comment',12,'delete_gradecomment'),(37,'Can add course content',13,'add_coursecontent'),(38,'Can change course content',13,'change_coursecontent'),(39,'Can delete course content',13,'delete_coursecontent'),(40,'Can add greeting',14,'add_greeting'),(41,'Can change greeting',14,'change_greeting'),(42,'Can delete greeting',14,'delete_greeting'),(43,'Can add quiz',15,'add_quiz'),(44,'Can change quiz',15,'change_quiz'),(45,'Can delete quiz',15,'delete_quiz'),(46,'Can add quiz question',16,'add_quizquestion'),(47,'Can change quiz question',16,'change_quizquestion'),(48,'Can delete quiz question',16,'delete_quizquestion'),(49,'Can add slide',17,'add_slide'),(50,'Can change slide',17,'change_slide'),(51,'Can delete slide',17,'delete_slide'),(52,'Can add activity',18,'add_activity'),(53,'Can change activity',18,'change_activity'),(54,'Can delete activity',18,'delete_activity'),(55,'Can add announcement',19,'add_announcement'),(56,'Can change announcement',19,'change_announcement'),(57,'Can delete announcement',19,'delete_announcement'),(58,'Can add announce read',20,'add_announceread'),(59,'Can change announce read',20,'change_announceread'),(60,'Can delete announce read',20,'delete_announceread'),(61,'Can add user profile',21,'add_userprofile'),(62,'Can change user profile',21,'change_userprofile'),(63,'Can delete user profile',21,'delete_userprofile'),(64,'Can add course',22,'add_course'),(65,'Can change course',22,'change_course'),(66,'Can delete course',22,'delete_course'),(67,'Can add class list',23,'add_classlist'),(68,'Can change class list',23,'change_classlist'),(69,'Can delete class list',23,'delete_classlist'),(70,'Can add upload user list',24,'add_uploaduserlist'),(71,'Can change upload user list',24,'change_uploaduserlist'),(72,'Can delete upload user list',24,'delete_uploaduserlist'),(73,'Can add upload class list',25,'add_uploadclasslist'),(74,'Can change upload class list',25,'change_uploadclasslist'),(75,'Can delete upload class list',25,'delete_uploadclasslist'),(76,'Can add setting',26,'add_setting'),(77,'Can change setting',26,'change_setting'),(78,'Can delete setting',26,'delete_setting'),(79,'Can add submission',27,'add_submission'),(80,'Can change submission',27,'change_submission'),(81,'Can delete submission',27,'delete_submission'),(82,'Can add quiz attempt',28,'add_quizattempt'),(83,'Can change quiz attempt',28,'change_quizattempt'),(84,'Can delete quiz attempt',28,'delete_quizattempt'),(85,'Can add quiz result',29,'add_quizresult'),(86,'Can change quiz result',29,'change_quizresult'),(87,'Can delete quiz result',29,'delete_quizresult'),(88,'Can add topics',30,'add_topics'),(89,'Can change topics',30,'change_topics'),(90,'Can delete topics',30,'delete_topics'),(91,'Can add messages',31,'add_messages'),(92,'Can change messages',31,'change_messages'),(93,'Can delete messages',31,'delete_messages');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'kma50','Kevin','Mann','kma50@sfu.ca','sha1$50247$bd48e1a4c417707a5b0167c74fbb887e45197db6',1,1,1,'2012-04-11 14:07:01','2012-04-09 22:13:02'),(2,'drf1','Derek','Fong','drf1@sfu.ca','sha1$007fa$f08b1ba704cf602056e3fda55acfdaa4cc132189',1,1,1,'2012-04-11 14:22:54','2012-04-09 22:14:10'),(3,'allisonn','Allison','Ng','allisonn@sfu.ca','sha1$7a54b$937d978cb080a1b9deda97b285dcd50c01eaa202',1,1,1,'2012-04-10 17:43:04','2012-04-09 22:14:48'),(4,'apike','Allen','Pike','apike@sfu.ca','sha1$ba760$10812fc7708b8de17215b95b245ec895165241f3',1,1,1,'2012-04-11 12:14:36','2012-04-09 22:15:29'),(5,'dnonis','Dave','Nonis','dnonis@sfu.ca','sha1$5e6ef$b48a6a8ad76dffcc8bdfd532b7f09a8344c048f7',0,1,0,'2012-04-10 23:03:39','2012-04-09 22:16:47'),(6,'rluongo','Roberto','Luongo','rluongo@sfu.ca','sha1$31860$a02d06c68b3aac5d4e659698b6508ba721cd072d',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(7,'hsedin','Henrik','Sedin','hsedin@sfu.ca','sha1$906ef$0f3a01fce43ae2695db3561fd15ece7a057c1ba5',0,1,0,'2012-04-11 14:01:04','2012-04-09 22:16:47'),(8,'dsedin','Daniel','Sedin','dsedin@sfu.ca','sha1$3aa4e$9ac3e07001ae31d6fbcc510f9cf37477784b71f1',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(9,'mnaslund','Marcus','Naslund','mnaslund@sfu.ca','sha1$3cd42$13ae247293fcc1f3d18bb77bb623d0b9b00a05ba',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(10,'rkesler','Ryan','Kesler','rkesler@sfu.ca','sha1$05d83$55e7789d0c047e488ff294d19b8e45e534d01d14',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(11,'aburrows','Alex','Burrows','aburrows@sfu.ca','sha1$e6bc0$abdb3f0988f3211c33379b81300c6f5207f0e2e4',0,1,0,'2012-04-10 01:00:31','2012-04-09 22:16:47'),(12,'tpyatt','Taylor','Pyatt','tpyatt@sfu.ca','sha1$deee7$28fb1eb4e6fcb551da4e2ec9f74e33d2592cb6c4',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(13,'bmorrison','Brenden','Morrison','bmorrison@sfu.ca','sha1$11be9$a86dc6eaac77693dbb275b5b5580c75f34622a57',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(14,'tlinden','Trevor','Linden','tlinden@sfu.ca','sha1$443ec$f15f7eacf18686f33b741d2d558e5c7aaefff37b',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(15,'jcowan','Jeff','Cowan','jcowan@sfu.ca','sha1$df70a$be1607396600570cbff9229c7b86d1cfb7af656e',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(16,'brichie','Byron','Richie','brichie@sfu.ca','sha1$0421d$3f5c0f5ea1b31646588c171c7c3742eb2f6557f1',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(17,'mraymond','Mason','Raymond','mraymond@sfu.ca','sha1$1ab9c$d7972a5bdb957fc4d3bc88775bd3e78803d154fd',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(18,'rshannon','Ryan','Shannon','rshannon@sfu.ca','sha1$a30cb$4c42cacb98ba02aea01ca6c8861a0fed6e06dc70',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(19,'mpettinger','Matt','Pettinger','mpettinger@sfu.ca','sha1$07781$f77da533d8cab46163f656a6fa997c10c824546d',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(20,'rrypien','Rick','Rypien','rrypien@sfu.ca','sha1$37091$98bcddf8f58db1f320a45d8c1405303b78b9f9a3',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(21,'cronning','Cliff','Ronning','cronning@sfu.ca','sha1$64167$65cce4d239b35c574467ff924d7341a9e23485bd',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(22,'dcloutier','Daniel','Cloutier','dcloutier@sfu.ca','sha1$b77cd$196ad4530d6eb2864923d5bd48770a3f3ac7f6db',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(23,'ejovo','Ed','Jovo','ejovo@sfu.ca','sha1$504d1$716908762dfb766ba8252fed9bca524962472a89',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(24,'pbure','Pavel','Bure','pbure@sfu.ca','sha1$6ce03$142b737227b6641c2d79710911eaec8fcb39fcbf',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(25,'mweaver','Mike','Weaver','mweaver@sfu.ca','sha1$1dd5b$fc9edb25570cdea2d89a039a3bfc938668b4df80',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(26,'nmciver','Nathan','Mciver','nmciver@sfu.ca','sha1$2094e$69b83d5660820f3f315e0e8c888b35f4ef7cb813',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(27,'lkrajicek','Lukas','Krajicek','lkrajicek@sfu.ca','sha1$0cac9$6da8feac16085e2dc8a2efffd63848104d45ad8f',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(28,'amiller','Aaron','Miller','amiller@sfu.ca','sha1$4c23c$6bc41ce5d7a0aa3699f3b550f35dc92192869311',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47'),(29,'lbourdon','Luc','Bourdon','lbourdon@sfu.ca','sha1$697ff$9a3d97649ff302cf2cf7c71ee3623dbab5c4687a',0,1,0,'2012-04-09 22:16:47','2012-04-09 22:16:47');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-04-09 22:13:49',1,3,'1','kma50',2,'Changed first_name and last_name. Added user profile \"556003392\".'),(2,'2012-04-09 22:14:10',1,3,'2','drf1',1,''),(3,'2012-04-09 22:14:19',1,3,'2','drf1',2,'Changed is_staff and is_superuser.'),(4,'2012-04-09 22:14:48',1,3,'3','allisonn',1,''),(5,'2012-04-09 22:14:55',1,3,'3','allisonn',2,'Changed is_staff and is_superuser.'),(6,'2012-04-09 22:15:29',1,3,'4','apike',1,''),(7,'2012-04-09 22:16:06',1,3,'4','apike',2,'Changed is_staff and is_superuser.'),(8,'2012-04-09 22:16:41',1,24,'1','Master List',1,''),(9,'2012-04-09 22:18:41',1,22,'None','CMPT470 Spring2012 E100',1,''),(10,'2012-04-09 22:22:06',1,22,'None','CMPT470 Spring2012 E100',1,''),(11,'2012-04-09 22:42:04',1,22,'1','CMPT470 Spring2012 E100',1,''),(12,'2012-04-09 22:42:24',1,23,'1','ClassList object',1,''),(13,'2012-04-09 22:42:40',1,23,'2','ClassList object',1,''),(14,'2012-04-09 22:42:50',1,23,'3','ClassList object',1,''),(15,'2012-04-09 22:42:59',1,23,'4','ClassList object',1,''),(16,'2012-04-09 22:44:00',1,22,'2','CMPT404 Spring2012 D100',1,''),(17,'2012-04-09 22:45:00',1,22,'3','ENGL765 Spring2011 D100',1,''),(18,'2012-04-09 22:45:24',1,22,'4','CMPT471 Spring2012 D100',1,''),(19,'2012-04-09 22:45:43',1,25,'1','UploadClassList object',1,''),(20,'2012-04-09 22:46:03',1,25,'2','UploadClassList object',1,''),(21,'2012-04-09 22:46:38',1,23,'15','ClassList object',1,''),(22,'2012-04-09 22:46:51',1,23,'16','ClassList object',1,''),(23,'2012-04-09 22:47:04',1,23,'17','ClassList object',1,''),(24,'2012-04-09 22:47:31',1,23,'18','ClassList object',1,''),(25,'2012-04-09 22:47:47',1,23,'18','ClassList object',2,'Changed is_instructor and is_ta.'),(26,'2012-04-09 22:48:39',4,23,'19','ClassList object',1,''),(27,'2012-04-09 22:58:52',1,23,'20','ClassList object',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'label','Calendar','label'),(10,'event','Calendar','event'),(11,'grade','Gradebook','grade'),(12,'grade comment','Gradebook','gradecomment'),(13,'course content','Instructor','coursecontent'),(14,'greeting','Instructor','greeting'),(15,'quiz','Instructor','quiz'),(16,'quiz question','Instructor','quizquestion'),(17,'slide','Instructor','slide'),(18,'activity','Instructor','activity'),(19,'announcement','Instructor','announcement'),(20,'announce read','Instructor','announceread'),(21,'user profile','Main','userprofile'),(22,'course','Main','course'),(23,'class list','Main','classlist'),(24,'upload user list','Main','uploaduserlist'),(25,'upload class list','Main','uploadclasslist'),(26,'setting','Main','setting'),(27,'submission','Student','submission'),(28,'quiz attempt','Student','quizattempt'),(29,'quiz result','Student','quizresult'),(30,'topics','Forum','topics'),(31,'messages','Forum','messages');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('a2097cd35e99578b3de5a5d4c5869f19','YzgxMjQyZDYyYWIxYzM0ZGRhZWJkOTg4Yzk0MzAyNGEyZTk3MGRhYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-04-24 22:10:19'),('3a795fb5d9ebdf8f73e30bcd4543313e','YzgxMjQyZDYyYWIxYzM0ZGRhZWJkOTg4Yzk0MzAyNGEyZTk3MGRhYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-04-25 13:16:04'),('c7fadf9ecbe0151dd8677cf2db604247','MTUyNjZiY2UyMWFjNGQ4OTY2YjExYjI0NzBlNDU2NGVkZjdiZTM5NjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-24 01:08:40'),('e018d8dc50998078b1dc9da03db9532e','ZTlhNmZkODJiMGIzMDg1YjI3OGE1ZTgxYWI4ZjM1NDNhMGNlNTZjYTqAAn1xAVgHAAAAZmxhdm91\nclgGAAAAbW9iaWxlcQJzLg==\n','2012-04-25 11:21:11'),('ee90dd8c6554fd8563814e6ed6198c25','MjkxZjQ2M2JkNmRiMGM5ZjA3ODllYWRiYTcwMmYyYWFmZjU3MjgzMTqAAn1xAS4=\n','2012-04-25 14:02:12'),('815cde084b3433c975f2a3dffa32e379','NmJjMDBiMzVjOGU0MmZiYjg4YjQwOWRiZjA4MThkNWI3MzhiNmMwNzqAAn1xAShYBwAAAGZsYXZv\ndXJYBAAAAGZ1bGxxAlUSX2F1dGhfdXNlcl9iYWNrZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZFUNX2F1dGhfdXNlcl9pZIoBAXUu\n','2012-04-24 11:37:04'),('41f96ce8630b80294422b06cd2643ea4','MjkxZjQ2M2JkNmRiMGM5ZjA3ODllYWRiYTcwMmYyYWFmZjU3MjgzMTqAAn1xAS4=\n','2012-04-24 15:03:49'),('17d2c34b076bdcccd20685c4a3546221','YzgxMjQyZDYyYWIxYzM0ZGRhZWJkOTg4Yzk0MzAyNGEyZTk3MGRhYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-04-24 16:51:03'),('7ad3f4b92ce353db1d42c46b73968ddf','M2JmNzM5NzQyNDY1NmFlYzY3MmU1MmRkNTRkYmQ1MWEzMGI4NDBjZTqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNYBwAAAGZsYXZvdXJYBgAAAG1vYmlsZXUu\n','2012-04-24 18:26:51'),('84a2aa0f611888c409207dd5cb4d527e','MTUyNjZiY2UyMWFjNGQ4OTY2YjExYjI0NzBlNDU2NGVkZjdiZTM5NjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-24 17:43:04'),('5075049ed9feb436c4089e070dc52ba8','ODlhOTU4ZGM1NzYzMDExODAxYzJkYzNkMDI3NDk4N2VmNjQ1N2U0ZDqAAn1xAVgHAAAAZmxhdm91\nclgEAAAAZnVsbHECcy4=\n','2012-04-24 18:26:55'),('75e401d43707a0dae3aa9c1af5dcdaf4','YzgxMjQyZDYyYWIxYzM0ZGRhZWJkOTg4Yzk0MzAyNGEyZTk3MGRhYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-04-25 12:18:39'),('36db4e43b67d8d55322bcf2e8f3c455d','MjkxZjQ2M2JkNmRiMGM5ZjA3ODllYWRiYTcwMmYyYWFmZjU3MjgzMTqAAn1xAS4=\n','2012-04-24 20:09:55'),('a0697b0c19759a7b735c181d63c1db5a','NzFiMzVkMjZiOWY2OTk0OWFmZGJmMDIwZmZiNjBiZGVmYTM2ZTdmNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-25 11:22:24'),('965de9c6ef5f585eec61bef3361b1113','NzFiMzVkMjZiOWY2OTk0OWFmZGJmMDIwZmZiNjBiZGVmYTM2ZTdmNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-25 14:22:54'),('5878b23c412a86635dca3371a389fcde','NmJjMDBiMzVjOGU0MmZiYjg4YjQwOWRiZjA4MThkNWI3MzhiNmMwNzqAAn1xAShYBwAAAGZsYXZv\ndXJYBAAAAGZ1bGxxAlUSX2F1dGhfdXNlcl9iYWNrZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZFUNX2F1dGhfdXNlcl9pZIoBAXUu\n','2012-04-25 14:38:23');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-11 14:40:34
