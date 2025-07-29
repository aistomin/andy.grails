#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Andy Grails Application..."

# Get the current submodule revisions
echo "📋 Getting submodule revisions..."

# Get backend revision (first 7 characters of the commit hash)
BACKEND_REVISION=$(cd andy.grails.backend && git rev-parse --short HEAD)
echo "🔧 Backend revision: $BACKEND_REVISION"

# Get frontend revision (first 7 characters of the commit hash)
FRONTEND_REVISION=$(cd andy.grails.frontend && git rev-parse --short HEAD)
echo "🎨 Frontend revision: $FRONTEND_REVISION"

# Export the revision variables for docker-compose
export BACKEND_REVISION=$BACKEND_REVISION
export FRONTEND_REVISION=$FRONTEND_REVISION

echo "🐳 Starting containers with docker compose..."
echo "   Backend image: andygrails/andy-grails-backend:$BACKEND_REVISION"
echo "   Frontend image: andygrails/andy-grails-frontend:$FRONTEND_REVISION"

# Start the application using docker compose
docker compose up -d

echo "✅ Application started successfully!"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔌 Backend API: http://localhost:8080"
echo "🗄️  Database: localhost:55432"
echo ""
echo "📊 To view logs: docker compose logs -f"
echo "🛑 To stop: ./stop.sh" 