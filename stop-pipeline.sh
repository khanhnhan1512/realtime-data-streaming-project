#!/bin/bash

# Stop Realtime Data Streaming Pipeline
echo "🛑 Stopping Realtime Data Streaming Pipeline..."

echo "1️⃣ Stopping Spark and Cassandra..."
docker compose -f docker-compose.spark.yaml down -v

# Stop Airflow first (reverse order)
echo "2️⃣ Stopping Airflow..."
docker compose -f docker-compose.airflow3.yaml down -v

# Stop Kafka infrastructure
echo "3️⃣ Stopping Kafka infrastructure..."
docker compose -f docker-compose.kafka.yaml down -v

echo "✅ Pipeline stopped successfully!"
echo "🧹 All containers and volumes have been removed."