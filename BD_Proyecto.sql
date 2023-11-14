CREATE DATABASE IF NOT EXISTS db_api_proyecto;
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

INSERT INTO Usuario VALUES
(1,'pepe10','123456','Jose Lopez',154211223,'pepe@gmail.com'),
(2,'diego30','012345','Diego Leal',155435321,'eldiego@gmail.com');

CREATE TABLE IF NOT EXISTS Cliente(
    id_cliente INT(10) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    dni INT(8) NOT NULL,
    activo BOOLEAN NOT NULL,
    PRIMARY KEY (id_cliente)
);

CREATE TABLE IF NOT EXISTS Producto(
    id_producto INT(10) NOT NULL AUTO_INCREMENT,
    nombre_producto VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    precio INT(8) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    stock INT(8),
    vendidos_producto INT(8) NOT NULL,
    PRIMARY KEY (id_producto)
);