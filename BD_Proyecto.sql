CREATE DATABASE IF NOT EXISTS  db_api_proyecto;
USE db_api_proyecto;

CREATE TABLE IF NOT EXISTS Usuario(
    id_user INT(10) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,

)
