CREATE DATABASE certificate_system;

USE certificate_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    cert_type VARCHAR(50),
    income VARCHAR(50),
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
