#!/bin/bash
set -e

echo "Starting stack..."
docker compose down -v
docker compose up -d

echo "Waiting for services..."
until [ "$(docker inspect -f '{{.State.Running}}' weather-n8n 2>/dev/null)" == "true" ] && \
      [ "$(docker inspect -f '{{.State.Running}}' weather-ollama 2>/dev/null)" == "true" ]; do
    sleep 2
done

sleep 5

echo "Pulling Ollama model..."
docker exec weather-ollama ollama pull llama3

echo "Importing Credentials and Workflows into n8n..."
docker exec weather-n8n n8n import:credentials --input=/data/workflows/../credentials.json || true
docker exec weather-n8n n8n import:workflow --separate --input=/data/workflows

echo "Stack is fully initialized and active!"
