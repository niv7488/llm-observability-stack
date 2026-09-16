#!/bin/bash
set -e

echo "Starting stack..."
docker compose down -v
docker compose build agent-ui
docker compose up -d

echo "Waiting for services..."
until [ "$(docker inspect -f '{{.State.Running}}' weather-n8n 2>/dev/null)" == "true" ] && \
      [ "$(docker inspect -f '{{.State.Running}}' weather-ollama 2>/dev/null)" == "true" ]; do
    sleep 2
done

sleep 5

echo "Pulling Ollama model..."
docker exec weather-ollama ollama pull llama3

echo "Importing Credentials into n8n..."
docker exec weather-n8n n8n import:credentials --input=/data/n8n/credentials.json || true

echo "Importing Workflows into n8n..."
docker exec weather-n8n n8n import:workflow --separate --input=/data/n8n/workflows

echo ""
echo "=================================================="
echo "      🚀 Stack is fully active & ready! 🚀       "
echo "=================================================="
echo " 🌐 Agent UI (Streamlit): http://localhost:8501"
echo " ⚡ n8n Workflows:        http://localhost:5678"
echo " 📊 Grafana Dashboards:   http://localhost:3000  (user: admin / pass: admin)"
echo " 📈 Prometheus Metrics:  http://localhost:9090"
echo " 🦙 Ollama API:          http://localhost:11434"
echo " 🐰 RabbitMQ Management: http://localhost:15672 (user: guest / pass: guest)"
echo " 🐘 Postgres Database:   localhost:5432          (db: weather_db / user: user)"
echo "=================================================="
echo ""
