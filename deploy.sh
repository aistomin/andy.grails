#!/bin/bash

# Exit on any error
set -e

# Function to display usage
usage() {
    echo "Usage: $0 <git-revision>"
    echo ""
    echo "Deploys the application to a specific Git revision."
    echo ""
    echo "Arguments:"
    echo "  git-revision    Git revision (commit hash, branch name, or tag)"
    echo ""
    echo "Examples:"
    echo "  $0 main"
    echo "  $0 abc1234"
    echo "  $0 v1.0.0"
    echo ""
    echo "The script will:"
    echo "  1. Check for local changes"
    echo "  2. Checkout the specified revision"
    echo "  3. Stop the current application"
    echo "  4. Start the application with new revision"
}

# Check if revision argument is provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Git revision is required"
    echo ""
    usage
    exit 1
fi

REVISION=$1

echo "🚀 Deploying Andy Grails Application revision: $REVISION"
echo ""

# Step 1: Check for local changes
echo "📋 Checking for local changes..."
if ! git diff-index --quiet HEAD --; then
    echo "❌ Error: There are uncommitted local changes in the repository."
    echo "   Please commit or stash your changes before deploying."
    echo ""
    echo "   To see the changes: git status"
    echo "   To stash changes: git stash"
    echo "   To commit changes: git add . && git commit -m 'your message'"
    exit 1
fi

# Check for untracked files
if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    echo "❌ Error: There are untracked files in the repository."
    echo "   Please add and commit them or add them to .gitignore before deploying."
    echo ""
    echo "   To see untracked files: git status"
    echo "   To add them: git add . && git commit -m 'your message'"
    exit 1
fi

echo "✅ No local changes detected"
echo ""

# Step 2: Check if the revision exists
echo "🔍 Checking if revision '$REVISION' exists..."
if ! git rev-parse --verify "$REVISION" >/dev/null 2>&1; then
    echo "❌ Error: Revision '$REVISION' does not exist in the repository."
    echo ""
    echo "   Available options:"
    echo "   - Use a valid commit hash"
    echo "   - Use a valid branch name"
    echo "   - Use a valid tag name"
    echo ""
    echo "   To see recent commits: git log --oneline -10"
    echo "   To see branches: git branch -a"
    echo "   To see tags: git tag"
    exit 1
fi

echo "✅ Revision '$REVISION' found"
echo ""

# Step 3: Checkout the revision
echo "📥 Checking out revision: $REVISION"
git checkout "$REVISION"

# Update submodules to match the revision
echo "📦 Updating submodules..."
git submodule update --init --recursive

echo "✅ Successfully checked out revision: $REVISION"
echo ""

# Step 4: Stop the current application
echo "🛑 Stopping current application..."
./stop.sh
echo ""

# Step 5: Start the application with new revision
echo "🚀 Starting application with new revision..."
./start.sh
echo ""

echo "🎉 Deployment completed successfully!"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔌 Backend API: http://localhost:8080"
echo "🗄️  Database: localhost:55432"
echo ""
echo "📊 To view logs: docker compose logs -f"
echo "🛑 To stop: ./stop.sh" 