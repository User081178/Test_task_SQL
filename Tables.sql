-- Создание базы данных

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

-- Создание таблицы клиентов
CREATE TABLE clients (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);

-- Добавление данных о клиентах
INSERT INTO clients (id, name, email) VALUES
(1, 'Анна', 'anna@anymail.com'),
(2, 'Иван', 'ivan@anymail.com'),
(3, 'Мария', 'maria@anymail.com'),
(4, 'Петр', 'petr@anymail.com'),
(5, 'Елена', 'elena@anymail.com');

-- Создание таблицы платежей
CREATE TABLE payments (
    id INT PRIMARY KEY NOT NULL,
    amount DECIMAL(10, 2),
    date DATE
);

-- Добавление данных о платежах
INSERT INTO payments (id, amount, date) VALUES
(101, 100.50, '2024-01-15'),
(205, 75.25, '2024-02-10'),
(306, 120.00, '2024-02-28'),
(412, 90.75, '2024-03-05'),
(523, 150.20, '2024-03-20');

-- Создание таблицы связей между клиентами и платежами
CREATE TABLE client_payment_relations (
    client_id INT,
    payment_id INT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (payment_id) REFERENCES payments(id),
    PRIMARY KEY (client_id, payment_id)
);

-- Добавление данных в таблицу связей между клиентами и платежами
INSERT INTO client_payment_relations (client_id, payment_id) VALUES
(1, 101),
(2, 205),
(3, 306),
(4, 412),
(5, 523);
