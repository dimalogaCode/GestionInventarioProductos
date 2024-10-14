CREATE DATABASE Inventario;
USE	 Inventario;


CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    cantidad INT,
    precio DECIMAL(10, 2)
);


select * from  productos;