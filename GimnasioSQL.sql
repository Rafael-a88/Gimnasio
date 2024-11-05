CREATE DATABASE Gimnasio;

USE Gimnasio;

CREATE TABLE Clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    edad INT NOT NULL,
    direccion VARCHAR (50) NOT NULL,
    telefono VARCHAR (9) NOT NULL
);

CREATE TABLE Aparatos (
    id INT auto_increment PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL
);

CREATE TABLE Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_dni VARCHAR (20) NOT NULL,
    aparato_id INT,
    hora_inicio DATETIME NOT NULL,
    hora_fin DATETIME NOT NULL,
    FOREIGN KEY (cliente_dni) REFERENCES Clientes(dni),
    FOREIGN KEY (aparato_id) REFERENCES Aparatos(id)
);

CREATE TABLE Pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    mes_pago VARCHAR(20),
    fecha_pago DATETIME,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
);
