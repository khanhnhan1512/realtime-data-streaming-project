#!/bin/bash

# Stop Realtime Data Streaming Pipeline
echo "🛑 Stopping Realtime Data Streaming Pipeline..."

# Stop Airflow first (reverse order)
echo "1️⃣ Stopping Airflow..."
docker compose -f docker-compose.airflow3.yaml down -v

# Stop Kafka infrastructure
echo "2️⃣ Stopping Kafka..."
docker compose -f docker-compose.yaml down -v

echo "✅ Pipeline stopped successfully!"
echo "🧹 All containers and volumes have been removed."