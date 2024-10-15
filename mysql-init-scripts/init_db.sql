-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS dishcovery_dev_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'dishcovery_dev'@'%' IDENTIFIED BY 'dishcovery_dev_pwd';

-- Grant all privileges to the user on the database
GRANT ALL PRIVILEGES ON dishcovery_dev_db.* TO 'dishcovery_dev'@'%';

-- Flush privileges to ensure the changes take effect
FLUSH PRIVILEGES;
