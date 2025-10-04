# Use Apache Airflow base image with Python 3.11
FROM apache/airflow:3.0.6-python3.11

# Switch to root to install system packages if needed
USER root

# Install any system dependencies if required
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements.txt
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy DAGs and source code
COPY airflow/dags /opt/airflow/dags
COPY api-request/src /opt/airflow/api-request/src
COPY script /opt/airflow/script

# Set working directory
WORKDIR /opt/airflow