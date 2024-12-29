# Realtime Data Streaming | End-to-End Data Engineering Project

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [What You'll Learn](#what-youll-learn)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Watch the Video Tutorial](#watch-the-video-tutorial)

## Introduction

This project serves as a comprehensive guide to building an end-to-end data engineering pipeline. It covers each stage from data ingestion to processing and finally to storage, utilizing a robust tech stack that includes Apache Airflow, Python, Apache Kafka (now using Kraft), Apache Spark, and Cassandra. Everything is containerized using Docker for ease of deployment and scalability. The project has been enhanced with new branching logic for gender detection within the Airflow DAGs.

## System Architecture

![System Architecture](https://github.com/airscholar/e2e-data-engineering/blob/main/Data%20engineering%20architecture.png)

The project is designed with the following components:

- 📄 **Data Source**: We use `randomuser.me` API to generate random user data for our pipeline.
- 🌀 **Apache Airflow**: Responsible for orchestrating the pipeline, including a new branching flow for gender detection, and storing fetched data in a PostgreSQL database.
- 🚀 **Apache Kafka (with Kraft)**: Used for streaming data from PostgreSQL to the processing engine. The setup now uses Kafka's native Kraft mode, removing the need for Zookeeper.
- 🎛️ **Control Center and Schema Registry**: Helps in monitoring and schema management of our Kafka streams.
- ⚙️ **Apache Spark**: For data processing with its master and worker nodes.
- 📦 **Cassandra**: Where the processed data will be stored.

## What You'll Learn

- 🛠️ Setting up a data pipeline with Apache Airflow
- 🌟 Implementing branching in Airflow DAGs for conditional workflows (e.g., gender detection)
- 📡 Real-time data streaming with Apache Kafka (using Kraft mode)
- 🔍 Data processing techniques with Apache Spark
- 💾 Data storage solutions with Cassandra and PostgreSQL
- 🐳 Containerizing your entire data engineering setup with Docker

## Technologies

- 🌀 Apache Airflow
- 🐍 Python
- 🚀 Apache Kafka (Kraft mode)
- ⚙️ Apache Spark
- 📦 Cassandra
- 🗄️ PostgreSQL
- 🐳 Docker

## Getting Started

1. 🖥️ Clone the repository:
    ```bash
    git clone https://github.com/airscholar/e2e-data-engineering.git
    ```

2. 📂 Navigate to the project directory:
    ```bash
    cd e2e-data-engineering
    ```

3. ⚙️ Update the `docker-compose.yml` file to use Kraft mode for Kafka. Ensure you pull the latest repository version if these changes are already integrated.

4. 🏗️ Run Docker Compose to spin up the services:
    ```bash
    docker-compose up
    ```

### Additional Notes for Deployment
- 🌀 The Airflow DAGs include a new branching logic for gender detection. Ensure the dependencies and conditions are correctly set in `dags/gender_detection_dag.py`.
- 🚀 Kafka's Kraft mode eliminates the need for Zookeeper, simplifying the setup and reducing resource usage. Ensure the `docker-compose.yml` aligns with the updated configuration.

---

### Fork-Friendly Version

If you plan to fork this repository, include the following changes:

- 📄 Document the new Airflow branching logic for gender detection in the `README.md`.
- 🛠️ Replace Zookeeper references in all documentation with Kafka's Kraft mode configurations.
- ✅ Test the updated pipeline to ensure compatibility with the forked repository setup.

### Self-Deployment Version

For self-deployment, follow these steps:

- ⚙️ Verify the `docker-compose.yml` includes the updated Kraft configuration for Kafka.
- 🗂️ Ensure the `dags/` directory contains the updated DAGs for branching workflows.
- 🌀 Run the full pipeline and validate the gender detection branching logic in the Airflow UI.

By tailoring the instructions and setup verification for each audience, the README stays clear and actionable for both contributors and independent users.

