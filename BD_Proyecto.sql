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
CREATE TABLE IF NOT EXISTS Cliente(
    id_cliente INT(10) NOT NULL AUTO_INCREMENT,
    id_usuario INT(10) ,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    dni INT(8) NOT NULL,
    activo BOOLEAN NOT NULL,
    PRIMARY KEY (id_cliente),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_user)
);

CREATE TABLE IF NOT EXISTS Producto(
    id_producto INT(10) NOT NULL AUTO_INCREMENT,
    id_usuario INT(10) ,
    nombre_producto VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    precio INT(8) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    stock INT(8),
    vendidos_producto INT(8) NOT NULL,
    PRIMARY KEY (id_producto),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_user)
);

CREATE TABLE IF NOT EXISTS Facturas(
    id_factura INT(10) NOT NULL AUTO_INCREMENT,
    id_cliente INT(10),
    hora_fecha DATETIME,
    descuento INT(5),
    TOTAL INT(10),
    PRIMARY KEY(id_factura),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE IF NOT EXISTS Detalle_factura(
    id_detalle INT(10) NOT NULL AUTO_INCREMENT,
    id_factura INT(10),
    id_producto INT(10),
    cantidad INT(8),
    precio INT(8),
    subtotal INT(10),
    PRIMARY KEY(id_detalle),
    FOREIGN KEY(id_factura) REFERENCES facturas(id_factura),
    FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
);