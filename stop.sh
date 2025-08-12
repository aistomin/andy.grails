#!/bin/bash

echo "🛑 Stopping Andy Grails Application..."

# Stop all containers using docker compose
docker compose down --remove-orphans

echo "✅ Application stopped successfully!"
echo ""
echo "🗑️  To remove volumes as well: docker compose down -v" 