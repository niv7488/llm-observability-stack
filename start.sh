#!/bin/bash
echo "🚀 Initializing Stack..."

# Launch containers
docker compose up -d --build

echo "⏳ Pulling llama3 model into Ollama container..."
docker exec -i weather-ollama ollama pull llama3

echo "✅ Deployment Complete!"
echo "--------------------------------------------------"
echo "🤖 Agent Interface:  http://localhost:8501"
echo "🔄 n8n Engine:       http://localhost:5678"
echo "📊 Grafana:          http://localhost:3000 (admin/admin)"
echo "🔥 Prometheus:       http://localhost:9090"
echo "--------------------------------------------------"
