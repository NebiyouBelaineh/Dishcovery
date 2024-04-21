-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dishcovery_dev_db;
CREATE USER IF NOT EXISTS 'dishcovery_dev'@'localhost' IDENTIFIED BY 'dishcovery_dev_pwd';
GRANT ALL PRIVILEGES ON `dishcovery_dev_db`.* TO 'dishcovery_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dishcovery_dev'@'localhost';
FLUSH PRIVILEGES;
