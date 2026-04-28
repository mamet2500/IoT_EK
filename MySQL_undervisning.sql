CREATE DATABASE IF NOT EXISTS iot_case_db;

USE iot_case_db;

DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS sensor_readings;
DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS turbines;
DROP TABLE IF EXISTS customers;

CREATE TABLE turbines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'active'
);

CREATE TABLE sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    threshold_value DECIMAL(10,2) NOT NULL DEFAULT 80.00,
    unit VARCHAR(20) NOT NULL DEFAULT 'mm/s',
    turbine_id INT NOT NULL,
    FOREIGN KEY (turbine_id) REFERENCES turbines(id)
);

CREATE TABLE sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL DEFAULT 'SensorValueReceived',
    reading_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

CREATE TABLE incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    reading_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'high',
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id),
    FOREIGN KEY (reading_id) REFERENCES sensor_readings(id)
);

USE iot_case_db;
SELECT * FROM turbines;
SELECT * FROM sensors;
SELECT * FROM sensor_readings;
SELECT * FROM incidents;
