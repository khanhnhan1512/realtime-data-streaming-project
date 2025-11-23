<h1 align="center">Realtime Data Streaming Pipeline</h1>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.vi.md">Tiếng Việt</a>
</p>

This is a personal project to build a real-time streaming pipeline using `Apache Kafka`, `Apache Spark Streaming`, and `Apache Airflow`. The goal of this pipeline is to collect user data from a mock API, process the data in real-time, and store it in a `Cassandra` database.

There is no complex data processing in this pipeline; the purpose of this project is simply to become familiar with using popular tools in the field of big data processing and real-time streaming.

# Table of Contents
- [Overview](#overview)
- [Pipeline Architecture](#pipeline-architecture)
- [Folder Structure](#folder-structure)
- [Data Flow](#data-flow)
- [Technologies Used](#technologies-used)
- [Installation Requirements](#installation-requirements)
- [Installation and Setup Guide](#installation-and-setup-guide)
- [Monitoring and Management](#monitoring-and-management)

# Overview

This pipeline is built for learning purposes, aiming to familiarize with big data processing and real-time streaming tools. User data is simulated from a simple API, then sent to Kafka for real-time processing using Spark Streaming. Finally, the processed data is stored in a Cassandra database to serve future analytical purposes.

# Pipeline Architecture
![Pipeline Architecture](./images/pipeline-architecture.svg)

# Folder Structure
```
├── 📁 airflow
│   ├── 📁 dags                             # Contains DAGs for Apache Airflow
│   │   └── 🐍 kafka_stream.py
│   └── 🐳 Dockerfile                       # Dockerfile to build Airflow image
├── 📁 api-request                          
│   ├── 📁 src      # Package `user_data_api` as a package to run in local environment
│   │   ├── 📁 api_request.egg-info         
│   │   │   ├── 📄 PKG-INFO
│   │   │   ├── 📄 SOURCES.txt
│   │   │   ├── 📄 dependency_links.txt
│   │   │   ├── 📄 requires.txt
│   │   │   └── 📄 top_level.txt
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 user_data_api.py             # Script to fetch data from API
│   ├── 📝 README.md
│   ├── 🐍 __init__.py
│   ├── 🐍 main.py
│   └── ⚙️ pyproject.toml
├── 📁 config
│   └── 📄 airflow.cfg
├── 📁 images                               # Contains image files
│   ├── 📄 pipeline-architecture.drawio
│   ├── 🖼️ pipeline-architecture.png
│   └── 🖼️ pipeline-architecture.svg
├── 📁 script                  # Contains entrypoints for services
├── 📁 spark
│   ├── 🐳 Dockerfile          # Dockerfile to build custom Spark image
│   └── 🐍 spark_stream.py     # Script to run Spark job
├── ⚙️ .dockerignore
├── ⚙️ .gitignore
├── 📝 README.md
├── ⚙️ docker-compose.airflow3.yaml # Docker Compose for Apache Airflow
├── ⚙️ docker-compose.kafka.yaml    # Docker Compose for Apache Kafka
├── ⚙️ docker-compose.spark.yaml    # Docker Compose for Apache Spark
├── ⚙️ pyproject.toml               # Configuration file for virtual environment management using uv
├── 📄 requirements.txt             # File containing virtual environment dependencies
├── 📄 stop-pipeline.sh             # Shell script to stop the entire pipeline
└── 📄 uv.lock                      # Virtual environment lock file for uv
```

# Data Flow
1. Simulated user data is fetched from the [API](https://randomuser.me/api). This API provides random user data with information such as name, email address, country, etc.
2. Each user's data (record) is sent to a topic in Apache Kafka through a producer.
3. Apache Airflow is used to orchestrate the above 2 processes.
4. Apache Spark Streaming is configured to listen to the Kafka topic and receive data in real-time.
5. Data received from Kafka will be processed by Spark, streamed, and stored in the Cassandra database.

# Technologies Used
| Technology       | Function                                                                                    |
|------------------|---------------------------------------------------------------------------------------------|
| Docker           | Package and run all services                                                                |
| Apache Kafka     | Receive and store high-throughput records                                                   |
| Zookeeper        | Manage and coordinate Kafka Cluster                                                         |
| Schema Registry  | Manage and validate schemas for records sent to Kafka                                       |
| Control Center   | Interface to manage and monitor Kafka Cluster                                               |
| Spark Streaming  | Listen to a topic from Kafka and stream new data in the topic to Cassandra in real-time    |
| Apache Cassandra | Database to store real-time records                                                         |
| Apache Airflow   | Monitor and orchestrate tasks in the pipeline                                               |
| PostgreSQL       | Store metadata for Airflow                                                                  |

# Prerequisites
To run this project, you need:
- Docker and Docker Compose installed.
- Python 3.11
- Virtual environment with libraries as specified in `requirements.txt`.
- `.env` file containing environment variables to run `Airflow` services such as:
    - `AIRFLOW_UID`
    - `AIRFLOW_GID`
    - `AIRFLOW_PROJ_DIR`
    - `_AIRFLOW_WWW_USER_USERNAME`
    - `_AIRFLOW_WWW_USER_PASSWORD`

# Installation and Setup Guide
1. Clone this repository to your machine:
    ```bash
    git clone https://github.com/khanhnhan1512/realtime-data-streaming-project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd realtime-data-streaming-project
    ```
3. Create and activate virtual environment:
    - If using `uv`:
        ```bash
        uv init
        uv sync
        ```
    - If using `venv`:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
4. Run Docker Compose to start the entire pipeline:
    ```bash
    docker-compose -f docker-compose.kafka.yaml up -d # wait about 20s for Kafka to start
    docker-compose -f docker-compose.airflow3.yaml up -d  # wait about 20s to start Airflow
    docker-compose -f docker-compose.spark.yaml up -d  # start Spark
    ```
5. Submit Spark job:
    ```bash
    docker exec spark-master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --conf "spark.sql.adaptive.enabled=false" \
    --conf "spark.jars.ivy=/tmp/.ivy2" \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 \
    /opt/spark/apps/spark_stream.py
    ```
6. Stop the entire pipeline:
    ```bash
    ./stop-pipeline.sh
    ```

# Monitoring and Management
- Kafka Control Center: [http://localhost:9021](http://localhost:9021)
- Airflow Web UI: [http://localhost:8081](http://localhost:8081) (username and password are configured in `.env` file, default is admin/admin)
- Spark Web UI: [http://localhost:9090](http://localhost:9090)

# ✉️ Contact
Feel free to connect with me on the following platforms:
- Email: khanhnhan012@gmail.com
- [![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/nguyen.khanh.nhan.905779)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nhan-nguyen-b22023260/)