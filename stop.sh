#!/bin/bash
echo "🛑 Stopping and cleaning up all services..."
docker compose down -v --remove-orphans
