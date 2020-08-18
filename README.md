# passkeep_web-0.1

This is for educational purposes only. DO NOT use this for a personal password manager, but if you're on here, I would assume you know better than that. I would just feel bad if someone stumbled upon it somehow and made a mistake not knowing any better

You must install a mysql server locally and set the environment variables in main.py or manually set them are variables.

Then, you must run these commands on your mysql server:

CREATE DATABASE IF NOT EXISTS `passkeep_web` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `passkeep_web`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `entries` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `account_id` int,
  	`service` varchar(255) NOT NULL,
  	`username` varchar(100) NOT NULL,
  	`password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


Then in console navigate to project directory,
pip install -r requirement.txt

then, if on linux, run:
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run

if on powershell, run:
$env:FLASK_APP=main.py
$env:FLASK_DEBUG=1
flask run

then visit in browser localhost:5000/passkeep_web/
