-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: MoYun
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(32) NOT NULL COMMENT 'ISBN',
  `title` varchar(128) NOT NULL COMMENT '标题',
  `originTitle` varchar(128) DEFAULT NULL COMMENT '原作名',
  `subtitle` varchar(128) DEFAULT NULL COMMENT '副标题',
  `author` varchar(128) NOT NULL COMMENT '作者',
  `page` int DEFAULT NULL COMMENT '页数',
  `publishDate` date DEFAULT NULL COMMENT '出版日期',
  `publisher` varchar(32) DEFAULT NULL COMMENT '出版社',
  `description` text COMMENT '简介',
  `doubanScore` float DEFAULT NULL,
  `doubanID` varchar(24) NOT NULL,
  `type` enum('马列主义、毛泽东思想、邓小平理论','哲学、宗教','社会科学总论','政治、法律','军事','经济','文化、科学、教育、体育','语言、文字','文学','艺术','历史、地理','自然科学总论','数理科学和化学','天文学、地球科学','生物科学','医药、卫生','农业科学','工业技术','交通运输','航空、航天','环境科学、安全科学','综合性图书') DEFAULT NULL COMMENT '图书类型',
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `name` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (1,'9787508696010','老人与海','The Old Man and the Sea',NULL,'[美] 欧内斯特·海明威',264,'2018-11-01','中信出版社','“人可以被毁灭，但不能被打败。”一位老人孤身在海上捕鱼，八十四天一无所获，等终于钓到大鱼，用了两天两夜才将其刺死。返航途中突遭鲨鱼袭击，经过一天一夜的缠斗，大鱼仅存骨架。但老人并未失去希望和信心，休整之后，准备再次出海……\r\n编辑推荐\r\n◆ 海明威等了64年的中文译本终于来了！华语传奇作家鲁羊首次翻译外国经典，译稿出版前在各界名人中广泛流传，好评如潮，口碑爆棚。\r\n◆ 《老人与海》有声演读版音频，李蕾姐姐读经典演绎，用声音为你复活《老人与海》。\r\n◆ 附英文原版，校自海明威1952年亲自授权的美国Scribner原版定本！中英双语，超值典藏。\r\n◆ 国际当红女插画师SlavaShults，首次为中文版《老人与海》专门创作12副海报级手绘插图，带给你前所未有的阅读体验；随书附赠精1张精美明信片（一套10张随机送）。\r\n◆ “所有的原则自天而降：那就是你必须相信魔法，相信美，相信那些在百万个钻石中总结我们的人，相信此刻你手捧的鲁羊先生的译本，就是‘不朽’这个璀璨的词语给出的最好佐证。”——丁玲文学大奖、徐志摩诗歌金奖双奖得主何三坡\r\n◆“鲁羊的译文，其语言的简洁、节奏、语感、画面感和情感浓与淡的交错堪称完美，我感觉是海明威用中文写了《老人与海》，真棒！”——美籍华人知名学者、博士后导师邢若曦\r\n◆ 自1954年荣获诺贝尔文学奖至今，《老人与海》风靡全球，横扫每个必读经典书单，征服了亿万读者；据作家榜官方统计：截至2017年1月，113位诺贝尔文学奖得主作品中文版销量排行榜，海明威高居榜首，总销量突破550万册。\r\n◆ “人可以被毁灭，但不能被打败。”——本书作者海明威（诺贝尔文学奖、普利策奖双奖得主）',9,'30338134','文学'),(2,'9787535447340','文化苦旅',NULL,'余秋雨三十年散文自选集','余秋雨',287,'2014-04-01','长江文艺出版社','《文化苦旅》一书于1992年首次出版，是余秋雨先生1980年代在海内外讲学和考察途中写下的作品，是他的第一部文化散文集。全书主要包括两部分，一部分为历史、文化散文，另一部分为回忆散文。甫一面世，该书就以文采飞扬、知识丰厚、见解独到而备受万千读者喜爱。由此开创“历史大散文”一代文风，令世人重拾中华文化价值。他的散文别具一格，见常人所未见，思常人所未思，善于在美妙的文字中一步步将读者带入历史文化长河，启迪哲思，引发情致，具有极高的审美价值和史学、文化价值。书中多篇文章后入选中学教材。但由于此书的重大影响，在为余秋雨先生带来无数光环和拥趸的同时，也带来了数之不尽的麻烦和盗版。誉满天下，“谤”亦随身。余秋雨先生在身心俱疲之下，决定亲自修订、重编此书。\n新版《文化苦旅》作为余秋雨先生30年历史文化散文修订自选集，删掉旧版37篇文章中的13篇，新增文章17篇，其中入选教材的《道士塔》《莫高窟》《都江堰》等经典篇目全部经过改写、修订。新版内容与旧版相比，全新和改写的篇目达到三分之二以上，对新老读者都是一场全新的阅读体验和人文享受。堪称余秋雨30年来不懈的文化考察和人生思索的完美结晶。',8.2,'19940743','文学'),(3,'9787801656087','明朝那些事儿（1-9）',NULL,'限量版','当年明月',NULL,'2009-04-01','中国海关出版社','《明朝那些事儿》讲述从1344年到1644年，明朝三百年间的历史。作品以史料为基础，以年代和具体人物为主线，运用小说的笔法，对明朝十七帝和其他王公权贵和小人物的命运进行全景展示，尤其对官场政治、战争、帝王心术着墨最多。作品也是一部明朝政治经济制度、人伦道德的演义。',9.2,'3674537','历史、地理'),(4,'9787020084357','我与地坛',NULL,NULL,'史铁生',234,'2008-09-01','人民文学出版社','《我与地坛(纪念版)》是史铁生文学作品中，充满哲思又极为人性化的代表作之一。其前两段被纳入人民教育出版社的高一教材中。前两部分注重讲地坛和他与母亲的后悔，对中学生来说，这是一篇令人反思的优秀文章。',9.2,'6079389','文学');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '这条信息的ID',
  `senderID` int NOT NULL COMMENT '发信人ID',
  `receiverID` int NOT NULL COMMENT '收信人ID',
  `content` text NOT NULL COMMENT '发信内容',
  `sendTime` datetime NOT NULL COMMENT '发信时间',
  `isRead` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查看',
  PRIMARY KEY (`id`),
  KEY `chat_user_id_fk` (`senderID`),
  KEY `chat_user_id_fk2` (`receiverID`),
  CONSTRAINT `chat_user_id_fk` FOREIGN KEY (`senderID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chat_user_id_fk2` FOREIGN KEY (`receiverID`) REFERENCES `user` (`id`) ON DELETE SET DEFAULT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat`
--

LOCK TABLES `chat` WRITE;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `error` (
  `errorCode` int NOT NULL,
  `title` varchar(128) NOT NULL,
  `title_en` varchar(128) NOT NULL,
  `content` text NOT NULL,
  `publishTime` datetime NOT NULL,
  `authorID` int NOT NULL,
  `referenceLink` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`errorCode`),
  KEY `error_user_id_fk` (`authorID`),
  CONSTRAINT `error_user_id_fk` FOREIGN KEY (`authorID`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='该表用于存储定制的HTTP错误响应内容';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error`
--

LOCK TABLES `error` WRITE;
/*!40000 ALTER TABLE `error` DISABLE KEYS */;
/*!40000 ALTER TABLE `error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL COMMENT '圈子的名称',
  `founderID` int NOT NULL COMMENT '圈子创建者的ID',
  `establishTime` datetime NOT NULL,
  `description` text COMMENT '对该圈子的介绍',
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_name_uindex` (`name`),
  KEY `group_user_id_fk` (`founderID`),
  CONSTRAINT `group_user_id_fk` FOREIGN KEY (`founderID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='圈子(但是我觉得叫group更合适)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_discussion`
--

DROP TABLE IF EXISTS `group_discussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_discussion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `posterID` int NOT NULL,
  `groupID` int NOT NULL,
  `postTime` datetime NOT NULL COMMENT '创建时间',
  `title` varchar(256) NOT NULL COMMENT '帖子的标题',
  `content` text NOT NULL COMMENT '帖子内容',
  `isRead` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查看',
  PRIMARY KEY (`id`),
  KEY `group_discussion_group_id_fk` (`groupID`),
  KEY `group_discussion_user_id_fk` (`posterID`),
  CONSTRAINT `group_discussion_group_id_fk` FOREIGN KEY (`groupID`) REFERENCES `group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `group_discussion_user_id_fk` FOREIGN KEY (`posterID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='讨论贴-圈子桥接表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_discussion`
--

LOCK TABLES `group_discussion` WRITE;
/*!40000 ALTER TABLE `group_discussion` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_discussion_reply`
--

DROP TABLE IF EXISTS `group_discussion_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_discussion_reply` (
  `authorID` int NOT NULL COMMENT '作者ID',
  `discussionID` int NOT NULL COMMENT '讨论贴ID',
  `replyTime` datetime NOT NULL COMMENT '回复日期',
  `content` text NOT NULL COMMENT '回复内容',
  `isRead` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查看',
  PRIMARY KEY (`authorID`,`discussionID`,`replyTime`),
  KEY `discuss_reply_discuss_id_fk` (`discussionID`),
  CONSTRAINT `discuss_reply_discuss_id_fk` FOREIGN KEY (`discussionID`) REFERENCES `group_discussion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `discuss_reply_user_id_fk` FOREIGN KEY (`authorID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_discussion_reply`
--

LOCK TABLES `group_discussion_reply` WRITE;
/*!40000 ALTER TABLE `group_discussion_reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_discussion_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_user`
--

DROP TABLE IF EXISTS `group_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_user` (
  `userID` int NOT NULL,
  `groupID` int NOT NULL,
  `joinTime` datetime NOT NULL COMMENT '加入时间',
  PRIMARY KEY (`userID`,`groupID`),
  KEY `group_user_group_id_fk` (`groupID`),
  CONSTRAINT `group_user_group_id_fk` FOREIGN KEY (`groupID`) REFERENCES `group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `group_user_user_id_fk` FOREIGN KEY (`userID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户-圈子桥接表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_user`
--

LOCK TABLES `group_user` WRITE;
/*!40000 ALTER TABLE `group_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal`
--

DROP TABLE IF EXISTS `journal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `firstParagraph` text NOT NULL,
  `content` text NOT NULL,
  `publishTime` datetime NOT NULL,
  `authorID` int NOT NULL,
  `bookID` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `journal_user_id_fk` (`authorID`),
  KEY `journal_book_id_fk` (`bookID`),
  CONSTRAINT `journal_book_id_fk` FOREIGN KEY (`bookID`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `journal_user_id_fk` FOREIGN KEY (`authorID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal`
--

LOCK TABLES `journal` WRITE;
/*!40000 ALTER TABLE `journal` DISABLE KEYS */;
/*!40000 ALTER TABLE `journal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal_comment`
--

DROP TABLE IF EXISTS `journal_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journal_comment` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `publishTime` datetime NOT NULL COMMENT '发表日期',
  `authorID` int NOT NULL COMMENT '作者ID',
  `journalID` int NOT NULL COMMENT '书评ID',
  `content` text NOT NULL COMMENT '评论内容',
  `isRead` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查看',
  PRIMARY KEY (`id`),
  KEY `journal_comment_journal_id_fk` (`journalID`),
  KEY `journal_comment_user_id_fk` (`authorID`),
  CONSTRAINT `journal_comment_journal_id_fk` FOREIGN KEY (`journalID`) REFERENCES `journal` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `journal_comment_user_id_fk` FOREIGN KEY (`authorID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal_comment`
--

LOCK TABLES `journal_comment` WRITE;
/*!40000 ALTER TABLE `journal_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `journal_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal_like`
--

DROP TABLE IF EXISTS `journal_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journal_like` (
  `authorID` int NOT NULL COMMENT '作者ID',
  `journalID` int NOT NULL COMMENT '书评ID',
  `publishTime` datetime NOT NULL COMMENT '发表日期',
  PRIMARY KEY (`authorID`,`journalID`),
  KEY `journal_like_journal_id_fk` (`journalID`),
  CONSTRAINT `journal_like_journal_id_fk` FOREIGN KEY (`journalID`) REFERENCES `journal` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `journal_like_user_id_fk` FOREIGN KEY (`authorID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='一个角色只能给某个书评点1个赞';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal_like`
--

LOCK TABLES `journal_like` WRITE;
/*!40000 ALTER TABLE `journal_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `journal_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(24) NOT NULL COMMENT '用户名',
  `password` varchar(128) NOT NULL COMMENT '密码',
  `signature` varchar(128) NOT NULL DEFAULT '' COMMENT '签名档',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `telephone` varchar(11) DEFAULT NULL COMMENT '联系电话',
  `lastLoginTime` datetime DEFAULT NULL COMMENT '上次登录时间',
  `role` enum('student','teacher','admin') NOT NULL DEFAULT 'student' COMMENT '身份组',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-14 17:39:08
