CREATE DATABASE IF NOT EXISTS  db_api_proyecto;
USE db_api_proyecto;

CREATE TABLE IF NOT EXISTS Usuario(
    id_user INT(10) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    telefono INT(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY(id_user)
);
INSERT INTO Usuario VALUES(
    1,'pepe10','123456','Jose Lopez',154211223,'pepe@gmail.com'),
    (2,'diego30','012345','Diego Leal',155435321,'eldiego@gmail.com'
);