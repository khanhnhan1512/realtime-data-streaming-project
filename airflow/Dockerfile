# Use Apache Airflow base image with Python 3.11
FROM apache/airflow:3.0.6-python3.11

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