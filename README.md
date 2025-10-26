<h1 align="center">Realtime Data Streaming Pipeline</h1><h1 align="center">Realtime Data Streaming Pipeline</h1>



<p align="center">Đây là dự án cá nhân xây dựng một pipeline realtime streaming sử dụng `Apache Kafka`, `Apache Spark Streaming` và `Apache Airflow`. Mục tiêu của pipeline là thu thập dữ liệu người dùng từ một API giả lập, xử lý dữ liệu theo thời gian và lưu trữ chúng vào cơ sở dữ liệu `Cassandra`.

  <a href="README.md">English</a> ·

  <a href="README.vi.md">Tiếng Việt</a>Không có việc xử lý dữ liệu nào quá phức tạp trong pipeline này, mục đích của project này chỉ là để làm quen với việc sử dụng các công cụ phổ biến trong lĩnh vực xử lý dữ liệu lớn và realtime streaming.

</p>

# Mục lục

This is a personal project building a realtime streaming pipeline using `Apache Kafka`, `Apache Spark Streaming`, and `Apache Airflow`. The pipeline's goal is to collect user data from a mock API, process data in real-time, and store it in a `Cassandra` database.- [Tổng quan](#tổng-quan)

- [Kiến trúc pipeline](#kiến-trúc-pipeline)

There is no overly complex data processing in this pipeline; the project's purpose is simply to familiarize myself with common tools in the field of big data processing and realtime streaming.- [Cấu trúc thư mục](#cấu-trúc-thư-mục)

- [Luồng dữ liệu](#luồng-dữ-liệu)

# Table of Contents- [Công nghệ sử dụng](#công-nghệ-sử-dụng)

- [Overview](#overview)- [Yêu cầu cài đặt](#yêu-cầu-cài-đặt)

- [Pipeline Architecture](#pipeline-architecture)- [Hướng dẫn cài đặt và khởi chạy](#hướng-dẫn-cài-đặt-và-khởi-chạy)

- [Project Structure](#project-structure)- [Giám sát và quản lý](#giám-sát-và-quản-lý)

- [Data Flow](#data-flow)

- [Technologies Used](#technologies-used)# Tổng quan

- [Installation Requirements](#installation-requirements)

- [Installation and Launch Guide](#installation-and-launch-guide)Pipeline này được xây dựng nhằm mục đích học tập và làm quen với các công cụ xử lý dữ liệu lớn và realtime streaming. Dữ liệu người dùng được giả lập từ một API đơn giản, sau đó được gửi vào Kafka để xử lý theo thời gian thực bằng Spark Streaming. Cuối cùng, dữ liệu đã xử lý sẽ được lưu trữ vào cơ sở dữ liệu Cassandra để phục vụ cho các mục đích phân tích sau này.

- [Monitoring and Management](#monitoring-and-management)

# Kiến trúc pipeline

# Overview![Pipeline Architecture](./images/pipeline-architecture.svg)



This pipeline is built for learning purposes and to familiarize myself with big data processing and realtime streaming tools. User data is simulated from a simple API, then sent to Kafka for real-time processing using Spark Streaming. Finally, the processed data is stored in a Cassandra database for later analysis purposes.# Cấu trúc thư mục

```

# Pipeline Architecture├── 📁 airflow

![Pipeline Architecture](./images/pipeline-architecture.svg)│   ├── 📁 dags                             # chứa các DAGs cho Apache Airflow

│   │   └── 🐍 kafka_stream.py

# Project Structure│   └── 🐳 Dockerfile                       # Dockerfile để xây dựng image Airflow 

```├── 📁 api-request                          

├── 📁 airflow│   ├── 📁 src      # Đóng gói `user_data_api` thành 1 package để chạy trên môi trường local

│   ├── 📁 dags                             # contains DAGs for Apache Airflow│   │   ├── 📁 api_request.egg-info         

│   │   └── 🐍 kafka_stream.py│   │   │   ├── 📄 PKG-INFO

│   └── 🐳 Dockerfile                       # Dockerfile to build Airflow image │   │   │   ├── 📄 SOURCES.txt

├── 📁 api-request                          │   │   │   ├── 📄 dependency_links.txt

│   ├── 📁 src      # Package `user_data_api` as a package to run on local environment│   │   │   ├── 📄 requires.txt

│   │   ├── 📁 api_request.egg-info         │   │   │   └── 📄 top_level.txt

│   │   │   ├── 📄 PKG-INFO│   │   ├── 🐍 __init__.py

│   │   │   ├── 📄 SOURCES.txt│   │   └── 🐍 user_data_api.py             # Script lấy data từ API

│   │   │   ├── 📄 dependency_links.txt│   ├── 📝 README.md

│   │   │   ├── 📄 requires.txt│   ├── 🐍 __init__.py

│   │   │   └── 📄 top_level.txt│   ├── 🐍 main.py

│   │   ├── 🐍 __init__.py│   └── ⚙️ pyproject.toml

│   │   └── 🐍 user_data_api.py             # Script to fetch data from API├── 📁 config

│   ├── 📝 README.md│   └── 📄 airflow.cfg

│   ├── 🐍 __init__.py├── 📁 images                               # Chứa các file ảnh

│   ├── 🐍 main.py│   ├── 📄 pipeline-architecture.drawio

│   └── ⚙️ pyproject.toml│   ├── 🖼️ pipeline-architecture.png

├── 📁 config│   └── 🖼️ pipeline-architecture.svg

│   └── 📄 airflow.cfg├── 📁 script                  # Chứa entrypoint cho các service

├── 📁 images                               # Contains image files├── 📁 spark

│   ├── 📄 pipeline-architecture.drawio│   ├── 🐳 Dockerfile          # Dockerfile để xây dựng custom image Spark 

│   ├── 🖼️ pipeline-architecture.png│   └── 🐍 spark_stream.py     # Script chạy Spark job

│   └── 🖼️ pipeline-architecture.svg├── ⚙️ .dockerignore

├── 📁 script                  # Contains entrypoints for services├── ⚙️ .gitignore

├── 📁 spark├── 📝 README.md

│   ├── 🐳 Dockerfile          # Dockerfile to build custom Spark image ├── ⚙️ docker-compose.airflow3.yaml # Docker Compose cho Apache Airflow

│   └── 🐍 spark_stream.py     # Script to run Spark job├── ⚙️ docker-compose.kafka.yaml    # Docker Compose cho Apache Kafka

├── ⚙️ .dockerignore├── ⚙️ docker-compose.spark.yaml    # Docker Compose cho Apache Spark

├── ⚙️ .gitignore├── ⚙️ pyproject.toml               # File cấu hình quản lý môi trường ảo bằng uv

├── 📝 README.md├── 📄 requirements.txt             # File chứa các dependencies của môi trường ảo

├── ⚙️ docker-compose.airflow3.yaml # Docker Compose for Apache Airflow├── 📄 stop-pipeline.sh             # Shell script để dừng toàn bộ pipeline

├── ⚙️ docker-compose.kafka.yaml    # Docker Compose for Apache Kafka└── 📄 uv.lock                      # File khóa môi trường ảo của uv

├── ⚙️ docker-compose.spark.yaml    # Docker Compose for Apache Spark```

├── ⚙️ pyproject.toml               # Configuration file for managing virtual environment with uv# Luồng dữ liệu

├── 📄 requirements.txt             # File containing virtual environment dependencies1. Dữ liệu giả lập về người dùng được lấy từ [API](https://randomuser.me/api). API này cung cấp dữ liệu người dùng ngẫu nhiên với các thông tin như tên, địa chỉ email, quốc gia, v.v.

├── 📄 stop-pipeline.sh             # Shell script to stop the entire pipeline2. Dữ liệu của từng người dùng (record) được gửi đến một chủ đề (topic) trong Apache Kafka thông qua một producer.

└── 📄 uv.lock                      # Virtual environment lock file for uv3. Apache Airflow được sử dụng để điều phối 2 quá trình trên.

```4. Apache Spark Streaming được cấu hình để lắng nghe chủ đề Kafka và nhận dữ liệu theo thời gian thực.

5. Dữ liệu nhận được từ Kafka sẽ được Spark nhận, truyền đi và lưu trữ vào cơ sở dữ liệu Cassandra.

# Data Flow

1. Simulated user data is retrieved from the [API](https://randomuser.me/api). This API provides random user data with information such as name, email address, country, etc.# Công nghệ sử dụng

2. Each user's data (record) is sent to a topic in Apache Kafka through a producer.| Công nghệ        | Chức năng                                                                                      |

3. Apache Airflow is used to orchestrate the above 2 processes.|------------------|------------------------------------------------------------------------------------------------|

4. Apache Spark Streaming is configured to listen to the Kafka topic and receive data in real-time.| Docker           | Đóng gói và chạy toàn bộ các service                                                           |

5. Data received from Kafka will be received by Spark, transmitted, and stored in the Cassandra database.| Apache Kafka     | Tiếp nhận và lưu trữ các record với lưu lượng cao                                              |

| Zookeeper        | Quản lý, điều phối Kafka Cluster                                                               |

# Technologies Used| Schema Registry  | Quản lý và xác thực schema cho các record gửi tới Kafka                                        |

| Technology       | Function                                                                                       || Control Center   | Giao diện để quản lý và giám sát Kafka Cluster                                                 |

|------------------|------------------------------------------------------------------------------------------------|| Spark Streaming  | Lắng nghe 1 topic từ Kafka và truyền dữ liệu mới trong topic đến Cassandra theo thời gian thực |

| Docker           | Package and run all services                                                                   || Apache Cassandra | Cơ sở dữ liệu để lưu trữ record thời gian thực                                                 |

| Apache Kafka     | Receive and store high-volume records                                                          || Apache Airflow   | Giám sát và điều phối các công việc trong pipeline                                             |

| Zookeeper        | Manage and coordinate Kafka Cluster                                                            || PostgresSQL      | Lưu trữ metadata cho Airflow                                                                   |

| Schema Registry  | Manage and validate schema for records sent to Kafka                                           |# Yêu cầu cài đặt

| Control Center   | Interface to manage and monitor Kafka Cluster                                                  |Để chạy được project này cần các điều kiện sau:

| Spark Streaming  | Listen to a topic from Kafka and transmit new data in the topic to Cassandra in real-time     |- Cài đặt Docker và Docker Compose.

| Apache Cassandra | Database to store real-time records                                                            |- Python 3.11

| Apache Airflow   | Monitor and orchestrate jobs in the pipeline                                                   |- Môi trường ảo có các thư viện như trong `requirements.txt`.

| PostgreSQL       | Store metadata for Airflow                                                                     |- File `.env` chứa các biến môi trường để chạy được các service của `Airflow` như:

    - `AIRFLOW_UID`

# Installation Requirements    - `AIRFLOW_GID`

To run this project, the following conditions are required:    - `AIRFLOW_PROJ_DIR`

- Docker and Docker Compose installed.    - `_AIRFLOW_WWW_USER_USERNAME`

- Python 3.11    - `_AIRFLOW_WWW_USER_PASSWORD`

- Virtual environment with libraries as in `requirements.txt`.# Hướng dẫn cài đặt và khởi chạy

- `.env` file containing environment variables to run `Airflow` services such as:1. Clone repository này về máy của bạn:

    - `AIRFLOW_UID`    ```bash

    - `AIRFLOW_GID`    git clone https://github.com/khanhnhan1512/realtime-data-streaming-project.git

    - `AIRFLOW_PROJ_DIR`    ```

    - `_AIRFLOW_WWW_USER_USERNAME`2. Di chuyển vào thư mục dự án:

    - `_AIRFLOW_WWW_USER_PASSWORD`    ```bash

    cd realtime-data-streaming-project

# Installation and Launch Guide    ```

1. Clone this repository to your machine:3. Tạo và kích hoạt môi trường ảo:

    ```bash    - Nếu sử dụng `uv`:

    git clone https://github.com/khanhnhan1512/realtime-data-streaming-project.git        ```bash

    ```        uv init

2. Navigate to the project directory:        uv sync

    ```bash        ```

    cd realtime-data-streaming-project    - Nếu sử dụng `venv`:

    ```        ```bash

3. Create and activate virtual environment:        python3 -m venv venv

    - If using `uv`:        source venv/bin/activate

        ```bash        pip install -r requirements.txt

        uv init        ```

        uv sync4. Chạy Docker Compose để khởi động toàn bộ pipeline:

        ```    ```bash

    - If using `venv`:    docker-compose -f docker-compose.kafka.yaml up -d # đợi khoảng 20s để Kafka khởi động xong

        ```bash    docker-compose -f docker-compose.airflow3.yaml up -d  # đợi khoảng 20s để khởi động Airflow

        python3 -m venv venv    docker-compose -f docker-compose.spark.yaml up -d  # khởi động Spark

        source venv/bin/activate    ```

        pip install -r requirements.txt5. Dừng toàn bộ pipeline:

        ```    ```bash

4. Run Docker Compose to start the entire pipeline:    ./stop-pipeline.sh

    ```bash    ```

    docker-compose -f docker-compose.kafka.yaml up -d # wait about 20s for Kafka to start# Giám sát và quản lý

    docker-compose -f docker-compose.airflow3.yaml up -d  # wait about 20s to start Airflow- Control Center của Kafka: [http://localhost:9021](http://localhost:9021)

    docker-compose -f docker-compose.spark.yaml up -d  # start Spark- Giao diện web của Airflow: [http://localhost:8081](http://localhost:8081) (username và password được cấu hình trong file `.env`, mặc định là admin/admin)

    ```- Giao diện web của Spark: [http://localhost:9090](http://localhost:9090)
5. Stop the entire pipeline:
    ```bash
    ./stop-pipeline.sh
    ```

# Monitoring and Management
- Kafka Control Center: [http://localhost:9021](http://localhost:9021)
- Airflow web interface: [http://localhost:8081](http://localhost:8081) (username and password are configured in the `.env` file, default is admin/admin)
- Spark web interface: [http://localhost:9090](http://localhost:9090)
