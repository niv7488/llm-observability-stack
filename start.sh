#!/bin/bash
echo "🚀 Starting Full Weather LLM Observability Stack..."

# Build and start services
docker compose up -d --build

echo "⏳ Waiting for Ollama to pull llama3 model..."
docker exec -it weather-ollama ollama pull llama3

echo "✅ All Services Are Running!"
echo "--------------------------------------------------"
echo "🤖 Agent UI:     http://localhost:8501"
echo "🔄 n8n UI:        http://localhost:5678"
echo "📊 Grafana:       http://localhost:3000 (admin/admin)"
echo "🔥 Prometheus:    http://localhost:9090"
echo "--------------------------------------------------"
