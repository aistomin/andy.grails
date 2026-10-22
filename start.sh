#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Andy Grails Application..."

# Resolve the submodule revisions (first 7 characters of the commit hash).
# `git submodule status` reads the gitlink from the parent repo, so it works
# even when the submodules are not initialized, and it follows a submodule
# that is checked out at a different commit.
echo "📋 Getting submodule revisions..."

BACKEND_REVISION=$(git submodule status andy.grails.backend | cut -c2-8)
echo "🔧 Backend revision: $BACKEND_REVISION"

FRONTEND_REVISION=$(git submodule status andy.grails.frontend | cut -c2-8)
echo "🎨 Frontend revision: $FRONTEND_REVISION"

# Export the revision variables for docker-compose
export BACKEND_REVISION=$BACKEND_REVISION
export FRONTEND_REVISION=$FRONTEND_REVISION

echo "🐳 Starting containers with docker compose..."
echo "   Backend image: andygrails/andy-grails-backend:$BACKEND_REVISION"
echo "   Frontend image: andygrails/andy-grails-frontend:$FRONTEND_REVISION"

# Start the application using docker compose. The frontend depends on the
# backend being healthy, so this command only returns once the backend is up.
docker compose up -d

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔌 Backend API: http://localhost:8080"
echo "🗄️  Database: localhost:55432"
echo ""
echo "📊 To view logs: docker compose logs -f"
echo "🛑 To stop: ./stop.sh"
