#!/bin/bash
set -e

echo "Starting Docker stack..."
docker compose down -v
docker compose up -d

echo "Waiting for services to initialize..."
until [ "$(docker inspect -f '{{.State.Running}}' weather-ollama 2>/dev/null)" == "true" ] && \
      [ "$(docker inspect -f '{{.State.Running}}' weather-n8n 2>/dev/null)" == "true" ]; do
    sleep 2
done

sleep 5

echo "Pulling llama3 model into Ollama container..."
docker exec weather-ollama ollama pull llama3

echo "Importing Workflows into n8n..."
docker exec weather-n8n n8n import:workflow --separate --input=/data/workflows

echo "Done! All services, models, and workflows are completely provisioned."
