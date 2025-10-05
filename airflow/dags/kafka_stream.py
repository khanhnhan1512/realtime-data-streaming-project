import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


sys.path.append('/opt/airflow/api-request/src')

def safe_callable():
    try:
        from user_data_api import stream_data
        result = stream_data()
        print(f"Task completed successfully: {result}")
        return result
    except Exception as e:
        error_msg = f"Task failed in safe_callable: {str(e)}"
        print(error_msg)
        # Re-raise so Airflow knows the task failed
        raise Exception(error_msg)

default_args = {
    'owner': 'airscholar', 
    'start_date': datetime(2025, 10, 4), 
    'catchup': False,
    'retries': 2,  # Increased retries
    'retry_delay': timedelta(minutes=2),  # Shorter retry delay
    'retry_exponential_backoff': True,  # Exponential backoff for retries
    'max_retry_delay': timedelta(minutes=10),  # Maximum retry delay
}

dag = DAG(
    dag_id='user_data_kafka_stream',
    default_args=default_args,
    schedule=timedelta(minutes=30),
    description='A DAG to stream user data to Kafka',
)

with dag:
    
    # Main streaming task
    stream_task = PythonOperator(
        task_id="stream_user_data_from_api",
        python_callable=safe_callable,
    )
    
    # Set task dependencies
    stream_task