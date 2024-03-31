CREATE DATABASE linkedin0;
USE linkedin_webscraping1;

CREATE TABLE company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE job (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company_id INT,
    location VARCHAR(255),
    applicants INT,
    condition VARCHAR(255),
    time TIMESTAMP,
    skills VARCHAR(255),
    FOREIGN KEY (company_id) REFERENCES company(id)
);