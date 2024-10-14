-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dishcovery_dev_db;
CREATE USER IF NOT EXISTS 'dishcovery_dev'@'localhost' IDENTIFIED BY 'dishcovery_dev_pwd';

-- Select database
USE dishcovery_dev_db; 

-- Create users table

CREATE TABLE IF NOT EXISTS users (
	id VARCHAR(36) PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	email VARCHAR(128) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	firstname VARCHAR(60),
	lastname VARCHAR(60)                
);

CREATE TABLE IF NOT EXISTS bookmarks (
	id VARCHAR(36) PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	label TEXT NULL,
	source VARCHAR(60) NULL,
	image_link TEXT NULL,
	ingredients TEXT NULL,
	total_time FLOAT NULL DEFAULT 0,
	calories FLOAT NULL DEFAULT 0.0,
	`link` TEXT NULL,
	tags TEXT NULL,
	user_id VARCHAR(60) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

	FLUSH PRIVILEGES;
