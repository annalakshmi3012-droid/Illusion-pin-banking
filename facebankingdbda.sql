-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 26, 2025 at 07:01 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `facebankingdbda`
--

-- --------------------------------------------------------

--
-- Table structure for table `beneficiarytb`
--

CREATE TABLE `beneficiarytb` (
  `id` bigint(250) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `AccName` varchar(250) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `IfscCode` varchar(250) NOT NULL,
  `BankName` varchar(250) NOT NULL,
  `Address` varchar(2000) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `beneficiarytb`
--


-- --------------------------------------------------------

--
-- Table structure for table `multitb`
--

CREATE TABLE `multitb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Account` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `multitb`
--


-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(50) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Pin` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `Balance` decimal(20,2) NOT NULL,
  `BankName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `regtb`
--


-- --------------------------------------------------------

--
-- Table structure for table `temptb`
--

CREATE TABLE `temptb` (
  `id` bigint(10) NOT NULL auto_increment,
  `AccountNo` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `OTP` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `temptb`
--


-- --------------------------------------------------------

--
-- Table structure for table `transtb`
--

CREATE TABLE `transtb` (
  `id` bigint(20) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `BName` varchar(250) NOT NULL,
  `BAccountNo` varchar(250) NOT NULL,
  `Currency` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `Hash1` varchar(250) NOT NULL,
  `Hash2` varchar(250) NOT NULL,
  `Type` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `transtb`
--

