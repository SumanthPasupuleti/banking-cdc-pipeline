# banking-cdc-pipeline
Real-time modern data stack project for the banking domain with data generation, CDC, streaming, and cloud object storage
# Banking Modern Data Stack

## 📌 Project Overview

This project demonstrates an end-to-end modern data stack pipeline for a banking domain.  
We simulate customer, account, and transaction data, stream change events in real time, and store processed records in AWS S3 for downstream use.

## 🏗️ Architecture

Pipeline Flow:  
Data Generator → Simulates banking transactions, accounts, and customers using Faker.  
MySQL → Source OLTP database for banking records.  
Kafka + Debezium → Captures change data and streams it in real time.  
Python Consumer → Reads Kafka topics and uploads records to AWS S3.  
Docker → Containerized local development environment.  
GitHub Actions → Automates builds and workflow tasks.

## ⚡ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![Debezium](https://img.shields.io/badge/Debezium-FF6F00?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

## ✅ Key Features

MySQL OLTP: Source relational database with banking tables for customers, accounts, and transactions.  
Simulated banking system: customers, accounts, and transactions generated with Faker.  
Change Data Capture (CDC): via Kafka + Debezium capturing MySQL binlog changes.  
Kafka consumer: reads topics and writes processed data to AWS S3.  
Dockerized setup: runs the full stack locally with containers.  
CI/CD workflow: automation with GitHub Actions.

## 📂 Repository Structure

```text
banking-modern-datastack/
├── .github/workflows/         # CI/CD pipelines
├── Consumer/
│   └── kafka_to_s3.py
├── data-generator/            # Faker-based data simulator
│   └── data_gen_file.py
├── kafka-debezium/            # Kafka connector setup
│   └── generate_and_post_connector.py
├── docker-compose.yml         # Containerized infra
├── requirements.txt
└── README.md
```

## ⚙️ Step-by-Step Implementation

### 1. Data Simulation

Generated synthetic banking data (customers, accounts, transactions) using Faker.  
Inserted data into MySQL so the system behaves like a real transactional database.

### 2. Kafka + Debezium CDC

Set up Kafka Connect and Debezium to capture changes from MySQL.  
Streamed CDC events into Kafka topics and processed them with a Python consumer.

### 3. AWS S3 Storage

The consumer batches records and uploads them to AWS S3 in Parquet format.

### 4. CI/CD with GitHub Actions

GitHub Actions can be used for linting, tests, or deployment automation.

## 📊 Final Deliverables

Automated CDC pipeline from MySQL to AWS S3  
Python consumer for Kafka topic processing  
Synthetic banking dataset for demos  
Dockerized local development environment  
CI/CD workflow structure

## Author

Author: Sumanth Pasupuleti  
LinkedIn: Sumanth [(https://www.linkedin.com/in/sumanth-/)]
