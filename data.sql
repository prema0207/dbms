CREATE DATABASE certificate_system;

USE certificate_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    role ENUM('user','admin') DEFAULT 'user'
);

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    certificate_type ENUM('income','community'),
    details TEXT,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    certificate_file VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
