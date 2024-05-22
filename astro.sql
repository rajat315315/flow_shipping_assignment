CREATE DATABASE flow_shipping;

USE flow_shipping;

CREATE TABLE merchants (
    merchant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE carriers (
    carrier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    max_orders INT NOT NULL,
    max_pieces INT NOT NULL,
    cost_per_order DECIMAL(10, 2) NOT NULL
);

CREATE TABLE merchandise (
    merchandise_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT,
    pieces INT NOT NULL,
    shipped BOOLEAN DEFAULT FALSE,
    carrier_id INT,
    shipped_date DATE,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
    FOREIGN KEY (carrier_id) REFERENCES carriers(carrier_id)
);
