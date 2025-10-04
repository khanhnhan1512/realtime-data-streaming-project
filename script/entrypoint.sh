#!/bin/bash
set -e

# Initialize DAGs on scheduler startup
if [ "$1" = "scheduler" ]; then
  echo "Starting Airflow Scheduler with DAG initialization..."
  # Start scheduler in background
  airflow "$@" &
  SCHEDULER_PID=$!
  
  # Wait a bit for scheduler to start
  sleep 10
  
  # Force DAG discovery
  echo "Forcing DAG discovery..."
  airflow dags reserialize || echo "DAG reserialize failed, but continuing..."
  
  # Wait for the scheduler process
  wait $SCHEDULER_PID
else
  exec airflow "$@"
fi