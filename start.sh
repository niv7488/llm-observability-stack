#!/usr/bin/env bash
set -e

echo "🚀 Starting LLM Observability Stack..."

# Build and bring up containers in detached mode
docker compose up --build -d

echo ""
echo "✅ Stack successfully started!"
echo "--------------------------------------------------"
echo "🌐 LLM Agent API:      http://localhost:8000"
echo "📊 Metrics Endpoint:   http://localhost:8000/metrics"
echo "🔥 Prometheus UI:      http://localhost:9090"
echo "📈 Grafana Dashboard:  http://localhost:3000 (User: admin / Pass: admin)"
echo "--------------------------------------------------"
