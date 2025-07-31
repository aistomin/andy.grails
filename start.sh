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

echo "⏳ Waiting for backend to be healthy..."

# Function to check backend health
check_backend_health() {
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "   Attempt $attempt/$max_attempts: Checking backend health..."
        
        if curl -s -f http://localhost:8080/actuator/health >/dev/null 2>&1; then
            # Check if the response contains "status":"UP"
            if curl -s http://localhost:8080/actuator/health | grep -q '"status":"UP"'; then
                echo "✅ Backend is healthy!"
                return 0
            fi
        fi
        
        echo "   Backend not ready yet, waiting 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ Backend failed to become healthy within 60 seconds"
    echo "   Check logs with: docker compose logs backend"
    return 1
}

# Wait for backend to be healthy
if check_backend_health; then
    echo ""
    echo "✅ Application started successfully!"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔌 Backend API: http://localhost:8080"
echo "🗄️  Database: localhost:55432"
echo ""
echo "📊 To view logs: docker compose logs -f"
echo "🛑 To stop: ./stop.sh"
else
    echo ""
    echo "❌ Application startup failed!"
    echo "   Backend did not become healthy in time."
    echo "   You can still check the logs: docker compose logs -f"
    exit 1
fi 