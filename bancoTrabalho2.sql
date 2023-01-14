CREATE DATABASE  IF NOT EXISTS `compras_online` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `compras_online`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: compras_online
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
-- Table structure for table `carrinho_compras`
--

DROP TABLE IF EXISTS `carrinho_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrinho_compras` (
  `Id_Cli` int NOT NULL,
  `Id_Pro` int NOT NULL,
  `Qtd_Pro` int NOT NULL,
  KEY `Id_Cli` (`Id_Cli`),
  KEY `Id_Pro` (`Id_Pro`),
  CONSTRAINT `carrinho_compras_ibfk_1` FOREIGN KEY (`Id_Cli`) REFERENCES `cliente` (`Id_Cli`),
  CONSTRAINT `carrinho_compras_ibfk_2` FOREIGN KEY (`Id_Pro`) REFERENCES `produtos` (`Id_Pro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrinho_compras`
--

LOCK TABLES `carrinho_compras` WRITE;
/*!40000 ALTER TABLE `carrinho_compras` DISABLE KEYS */;
/*!40000 ALTER TABLE `carrinho_compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `Id_Cli` int NOT NULL AUTO_INCREMENT,
  `Usuario_Cli` varchar(50) NOT NULL,
  `Nome_Cli` varchar(50) DEFAULT NULL,
  `Status_Cli` varchar(50) DEFAULT NULL,
  `E_Mail_Cli` varchar(50) DEFAULT NULL,
  `Senha_Cli` varchar(50) DEFAULT NULL,
  `Cidade_Cli` varchar(50) DEFAULT NULL,
  `Bairro_Cli` varchar(50) DEFAULT NULL,
  `Estado_Cli` varchar(50) DEFAULT NULL,
  `CPF_cli` varchar(50) NOT NULL,
  `Telefone_Cli` varchar(50) DEFAULT NULL,
  `Data_nasc_Cli` date DEFAULT NULL,
  PRIMARY KEY (`Id_Cli`,`Usuario_Cli`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (33,'adriano','Adriano Gomes Cunha','ATIVO','adriano00@gmail.com','123','Rio de Janeiro','Vila da Penha','Rio de Janeiro','','2481-1360',NULL),(35,'Adriano.g.c','Adriano Gomes da Cunha','ATIVO','adriano.g.c00@gmail.com','1234','Rio de Janeiro','1234','Rio de Janeiro','157.958.037','(021) 96732-4401','2000-01-01'),(36,'qfq','Pedro Jardins','ATIVO','daf','qfq','qfq','qfq','*623*6262','qfqf','226454626262626261296111','2000-01-01'),(37,'3f3f','Jair Ventura','ATIVO','jair@gmail.com','3f3','f3ef','3f3','3f3f','3f3f','qfqq3ff','2000-01-01'),(38,'3f3','Felipe Silva','ATIVO','adriano00@ga.com','fff','Rio de Janeiro','Vila da Penha','Rio de Janeir','3f3f','2481-1360','2000-01-03'),(39,'wefadcscac','Diego Costa','ATIVO','diego@gmail.com','ada','Caxias','Vila da Penha','Rio de Janeir','wfddvc','3391-3169','2000-01-01');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `Id_Func` int NOT NULL AUTO_INCREMENT,
  `Usuario_Func` varchar(50) NOT NULL,
  `Nome_Func` varchar(50) DEFAULT NULL,
  `Senha_Func` varchar(50) DEFAULT NULL,
  `Gerente` bit(1) NOT NULL,
  `RG_func` varchar(50) DEFAULT NULL,
  `CPF_func` varchar(50) DEFAULT NULL,
  `E_mail_func` varchar(50) DEFAULT NULL,
  `Telefone_Func` varchar(50) DEFAULT NULL,
  `Data_nasc_func` date DEFAULT NULL,
  PRIMARY KEY (`Id_Func`,`Usuario_Func`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
INSERT INTO `funcionario` VALUES (8,'adriano','adriano','1234',_binary '','','12','ee',NULL,NULL),(10,'adriano.g.c','Adriano Cunha','29092000',_binary '\0','','157.958.037-82','adriano00@gmail.com','(021)96732-4401','2000-09-29');
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itens_pedidos`
--

DROP TABLE IF EXISTS `itens_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itens_pedidos` (
  `Id_Pedido` int NOT NULL AUTO_INCREMENT,
  `Id_Pro` int NOT NULL,
  `Qtd_Pro` int NOT NULL,
  PRIMARY KEY (`Id_Pedido`,`Id_Pro`),
  KEY `Id_Pro` (`Id_Pro`),
  CONSTRAINT `itens_pedidos_ibfk_1` FOREIGN KEY (`Id_Pro`) REFERENCES `produtos` (`Id_Pro`),
  CONSTRAINT `itens_pedidos_ibfk_2` FOREIGN KEY (`Id_Pedido`) REFERENCES `pedidos` (`Id_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itens_pedidos`
--

LOCK TABLES `itens_pedidos` WRITE;
/*!40000 ALTER TABLE `itens_pedidos` DISABLE KEYS */;
INSERT INTO `itens_pedidos` VALUES (11,10,10),(11,11,6),(12,10,9),(12,11,4),(13,10,4),(14,10,13),(14,11,17),(15,11,6),(16,10,17),(16,11,3),(17,10,3),(17,11,5),(18,10,3),(19,11,5),(20,11,3),(21,11,4),(22,10,3),(22,11,6),(23,11,4),(24,10,8),(25,10,4),(26,10,3),(27,10,3);
/*!40000 ALTER TABLE `itens_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagamento`
--

DROP TABLE IF EXISTS `pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamento` (
  `Cod_Pagto` int NOT NULL AUTO_INCREMENT,
  `Id_Pedido` int NOT NULL,
  `Metodo_Pagto` varchar(50) DEFAULT NULL,
  `Status_Pagto` varchar(50) DEFAULT NULL,
  `valor_pgto` float(10,2) DEFAULT NULL,
  `data_pgto` date DEFAULT NULL,
  PRIMARY KEY (`Cod_Pagto`),
  KEY `Id_Pedido` (`Id_Pedido`),
  CONSTRAINT `pagamento_ibfk_1` FOREIGN KEY (`Id_Pedido`) REFERENCES `pedidos` (`Id_Pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamento`
--

LOCK TABLES `pagamento` WRITE;
/*!40000 ALTER TABLE `pagamento` DISABLE KEYS */;
INSERT INTO `pagamento` VALUES (1,13,'PIX','APROVADO',50.00,'2022-12-20'),(2,13,'PIX','APROVADO',50.00,'2022-12-23'),(3,12,'PIX','APROVADO',200.00,'2022-12-23'),(4,12,'PIX','APROVADO',43.00,'2022-12-23'),(5,11,'PIX','APROVADO',230.00,'2022-12-23'),(6,11,'BOLETO','APROVADO',13.00,'2022-12-23'),(7,11,'BOLETO','APROVADO',1.00,'2022-12-23'),(8,13,'BOLETO','APROVADO',0.00,'2022-12-23'),(9,12,'PIX','APROVADO',0.00,'2022-12-23'),(10,14,'BOLETO','APROVADO',200.00,'2022-12-23'),(11,14,'BOLETO','APROVADO',201.50,'2022-12-23'),(12,15,'CARTÃO DE CREDITO','APROVADO',10.00,'2022-12-23'),(13,15,'CARTÃO DE CREDITO','APROVADO',15.00,'2022-12-23'),(14,15,'CARTÃO DE CREDITO','APROVADO',2.00,'2022-12-23'),(15,16,'BOLETO','APROVADO',200.00,'2022-12-23'),(16,16,'BOLETO','APROVADO',238.50,'2022-12-23'),(17,17,'PIX','APROVADO',50.00,'2022-12-23'),(18,17,'BOLETO','APROVADO',40.00,'2022-12-23'),(19,25,'CARTÃO DE DEBITO','APROVADO',100.00,'2022-12-23'),(20,17,'PIX','APROVADO',7.50,'2022-12-23'),(21,19,'PIX','APROVADO',22.50,'2022-12-23'),(22,18,'PIX','APROVADO',75.00,'2022-12-23'),(23,21,'PIX','APROVADO',18.00,'2022-12-23'),(24,24,'BOLETO','APROVADO',200.00,'2022-12-23'),(25,26,'CARTÃO DE DEBITO','APROVADO',75.00,'2022-12-23');
/*!40000 ALTER TABLE `pagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `Id_Pedido` int NOT NULL AUTO_INCREMENT,
  `Id_Cli` int NOT NULL,
  `Status_Ped` varchar(50) DEFAULT NULL,
  `Data_Ped` date DEFAULT NULL,
  `Valor_Total_Ped` float(10,2) DEFAULT NULL,
  `Pagamento_Realizado` float(10,2) NOT NULL,
  `Pagamento_Pendente` float(10,2) NOT NULL,
  PRIMARY KEY (`Id_Pedido`),
  KEY `Id_Cli` (`Id_Cli`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`Id_Cli`) REFERENCES `cliente` (`Id_Cli`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (11,33,'NA TRANSPORTADORA','2022-11-11',277.00,310.00,-33.00),(12,33,'NA TRANSPORTADORA','2021-12-11',243.00,243.00,0.00),(13,33,'ENTREGUE','2022-10-13',100.00,100.00,0.00),(14,33,'ENTREGUE','2022-09-15',401.50,401.50,0.00),(15,33,'PAGAMENTO APROVADO','2022-08-15',27.00,27.00,0.00),(16,33,'NA TRANSPORTADORA','2022-07-15',438.50,438.50,0.00),(17,33,'PAGAMENTO APROVADO','2022-06-16',97.50,97.50,0.00),(18,33,'PAGAMENTO APROVADO','2022-05-17',75.00,75.00,0.00),(19,33,'PAGAMENTO APROVADO','2022-04-17',22.50,22.50,0.00),(20,33,'AGUARGANDO PAGAMENTO','2022-03-17',13.50,0.00,13.50),(21,33,'PAGAMENTO APROVADO','2022-02-17',18.00,18.00,0.00),(22,33,'AGUARGANDO PAGAMENTO','2022-01-17',102.00,0.00,102.00),(23,33,'ENTREGUE','2022-10-17',18.00,0.00,18.00),(24,33,'PAGAMENTO APROVADO','2021-12-17',200.00,200.00,0.00),(25,35,'NA TRANSPORTADORA','2022-12-17',100.00,100.00,0.00),(26,33,'PAGAMENTO APROVADO','2022-12-23',75.00,75.00,0.00),(27,33,'AGUARGANDO PAGAMENTO','2022-12-23',75.00,0.00,75.00);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `Id_Pro` int NOT NULL AUTO_INCREMENT,
  `Nome_Pro` varchar(50) DEFAULT NULL,
  `Preco_Pro` float(10,2) DEFAULT NULL,
  `Marca_Pro` varchar(50) DEFAULT NULL,
  `Status_Pro` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Id_Pro`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (10,'Lapis',25.00,'Faber-Castell','EM ESTOQUE'),(11,'Caneta',4.50,'BIC','EM ESTOQUE');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-25 18:19:40
