<h1 align="center">Realtime Data Streaming Pipeline</h1>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.vi.md">Tiếng Việt</a>
</p>

Đây là dự án cá nhân xây dựng một pipeline realtime streaming sử dụng `Apache Kafka`, `Apache Spark Streaming` và `Apache Airflow`. Mục tiêu của pipeline là thu thập dữ liệu người dùng từ một API giả lập, xử lý dữ liệu theo thời gian và lưu trữ chúng vào cơ sở dữ liệu `Cassandra`.

Không có việc xử lý dữ liệu nào quá phức tạp trong pipeline này, mục đích của project này chỉ là để làm quen với việc sử dụng các công cụ phổ biến trong lĩnh vực xử lý dữ liệu lớn và realtime streaming.

# Mục lục
- [Tổng quan](#tổng-quan)
- [Kiến trúc pipeline](#kiến-trúc-pipeline)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Luồng dữ liệu](#luồng-dữ-liệu)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Yêu cầu cài đặt](#yêu-cầu-cài-đặt)
- [Hướng dẫn cài đặt và khởi chạy](#hướng-dẫn-cài-đặt-và-khởi-chạy)
- [Giám sát và quản lý](#giám-sát-và-quản-lý)

# Tổng quan

Pipeline này được xây dựng nhằm mục đích học tập và làm quen với các công cụ xử lý dữ liệu lớn và realtime streaming. Dữ liệu người dùng được giả lập từ một API đơn giản, sau đó được gửi vào Kafka để xử lý theo thời gian thực bằng Spark Streaming. Cuối cùng, dữ liệu đã xử lý sẽ được lưu trữ vào cơ sở dữ liệu Cassandra để phục vụ cho các mục đích phân tích sau này.

# Kiến trúc pipeline
![Pipeline Architecture](./images/pipeline-architecture.svg)

# Cấu trúc thư mục
```
├── 📁 airflow
│   ├── 📁 dags                             # chứa các DAGs cho Apache Airflow
│   │   └── 🐍 kafka_stream.py
│   └── 🐳 Dockerfile                       # Dockerfile để xây dựng image Airflow 
├── 📁 api-request                          
│   ├── 📁 src      # Đóng gói `user_data_api` thành 1 package để chạy trên môi trường local
│   │   ├── 📁 api_request.egg-info         
│   │   │   ├── 📄 PKG-INFO
│   │   │   ├── 📄 SOURCES.txt
│   │   │   ├── 📄 dependency_links.txt
│   │   │   ├── 📄 requires.txt
│   │   │   └── 📄 top_level.txt
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 user_data_api.py             # Script lấy data từ API
│   ├── 📝 README.md
│   ├── 🐍 __init__.py
│   ├── 🐍 main.py
│   └── ⚙️ pyproject.toml
├── 📁 config
│   └── 📄 airflow.cfg
├── 📁 images                               # Chứa các file ảnh
│   ├── 📄 pipeline-architecture.drawio
│   ├── 🖼️ pipeline-architecture.png
│   └── 🖼️ pipeline-architecture.svg
├── 📁 script                  # Chứa entrypoint cho các service
├── 📁 spark
│   ├── 🐳 Dockerfile          # Dockerfile để xây dựng custom image Spark 
│   └── 🐍 spark_stream.py     # Script chạy Spark job
├── ⚙️ .dockerignore
├── ⚙️ .gitignore
├── 📝 README.md
├── ⚙️ docker-compose.airflow3.yaml # Docker Compose cho Apache Airflow
├── ⚙️ docker-compose.kafka.yaml    # Docker Compose cho Apache Kafka
├── ⚙️ docker-compose.spark.yaml    # Docker Compose cho Apache Spark
├── ⚙️ pyproject.toml               # File cấu hình quản lý môi trường ảo bằng uv
├── 📄 requirements.txt             # File chứa các dependencies của môi trường ảo
├── 📄 stop-pipeline.sh             # Shell script để dừng toàn bộ pipeline
└── 📄 uv.lock                      # File khóa môi trường ảo của uv
```
# Luồng dữ liệu
1. Dữ liệu giả lập về người dùng được lấy từ [API](https://randomuser.me/api). API này cung cấp dữ liệu người dùng ngẫu nhiên với các thông tin như tên, địa chỉ email, quốc gia, v.v.
2. Dữ liệu của từng người dùng (record) được gửi đến một chủ đề (topic) trong Apache Kafka thông qua một producer.
3. Apache Airflow được sử dụng để điều phối 2 quá trình trên.
4. Apache Spark Streaming được cấu hình để lắng nghe chủ đề Kafka và nhận dữ liệu theo thời gian thực.
5. Dữ liệu nhận được từ Kafka sẽ được Spark nhận, truyền đi và lưu trữ vào cơ sở dữ liệu Cassandra.

# Công nghệ sử dụng
| Công nghệ        | Chức năng                                                                                      |
|------------------|------------------------------------------------------------------------------------------------|
| Docker           | Đóng gói và chạy toàn bộ các service                                                           |
| Apache Kafka     | Tiếp nhận và lưu trữ các record với lưu lượng cao                                              |
| Zookeeper        | Quản lý, điều phối Kafka Cluster                                                               |
| Schema Registry  | Quản lý và xác thực schema cho các record gửi tới Kafka                                        |
| Control Center   | Giao diện để quản lý và giám sát Kafka Cluster                                                 |
| Spark Streaming  | Lắng nghe 1 topic từ Kafka và truyền dữ liệu mới trong topic đến Cassandra theo thời gian thực |
| Apache Cassandra | Cơ sở dữ liệu để lưu trữ record thời gian thực                                                 |
| Apache Airflow   | Giám sát và điều phối các công việc trong pipeline                                             |
| PostgresSQL      | Lưu trữ metadata cho Airflow                                                                   |
# Yêu cầu cài đặt
Để chạy được project này cần các điều kiện sau:
- Cài đặt Docker và Docker Compose.
- Python 3.11
- Môi trường ảo có các thư viện như trong `requirements.txt`.
- File `.env` chứa các biến môi trường để chạy được các service của `Airflow` như:
    - `AIRFLOW_UID`
    - `AIRFLOW_GID`
    - `AIRFLOW_PROJ_DIR`
    - `_AIRFLOW_WWW_USER_USERNAME`
    - `_AIRFLOW_WWW_USER_PASSWORD`
# Hướng dẫn cài đặt và khởi chạy
1. Clone repository này về máy của bạn:
    ```bash
    git clone https://github.com/khanhnhan1512/realtime-data-streaming-project.git
    ```
2. Di chuyển vào thư mục dự án:
    ```bash
    cd realtime-data-streaming-project
    ```
3. Tạo và kích hoạt môi trường ảo:
    - Nếu sử dụng `uv`:
        ```bash
        uv init
        uv sync
        ```
    - Nếu sử dụng `venv`:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
4. Chạy Docker Compose để khởi động toàn bộ pipeline:
    ```bash
    docker-compose -f docker-compose.kafka.yaml up -d # đợi khoảng 20s để Kafka khởi động xong
    docker-compose -f docker-compose.airflow3.yaml up -d  # đợi khoảng 20s để khởi động Airflow
    docker-compose -f docker-compose.spark.yaml up -d  # khởi động Spark
    ```
5. Dừng toàn bộ pipeline:
    ```bash
    ./stop-pipeline.sh
    ```
# Giám sát và quản lý
- Control Center của Kafka: [http://localhost:9021](http://localhost:9021)
- Giao diện web của Airflow: [http://localhost:8081](http://localhost:8081) (username và password được cấu hình trong file `.env`, mặc định là admin/admin)
- Giao diện web của Spark: [http://localhost:9090](http://localhost:9090)