import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


sys.path.append('/opt/airflow/api-request/src')

def safe_callable():
    try:
        from user_data_api import stream_data
        return stream_data()
    except Exception as e:
        print(f"Error in safe_callable: {str(e)}")
        raise e

default_args = {
    'owner': 'airscholar', 
    'start_date': datetime(2025, 10, 4), 
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='user_data_kafka_stream',
    default_args=default_args,
    schedule=timedelta(minutes=30),
    description='A DAG to stream user data to Kafka',
)

with dag:
    task_1 = PythonOperator(
        task_id="stream_user_data_from_api",
        python_callable=safe_callable,
    )