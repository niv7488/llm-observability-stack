#!/usr/bin/env bash
set -e

echo "🛑 Shutting down LLM Observability Stack..."

# Stop and remove containers, networks, and volumes
docker compose down -v --remove-orphans

echo "✅ Stack stopped and cleaned up successfully!"
