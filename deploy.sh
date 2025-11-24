#!/bin/bash

echo "🌊 Blue Whisper Ocean Club Bot - Deployment"
echo "============================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose first"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your TELEGRAM_BOT_TOKEN"
    exit 1
fi

echo "✅ All prerequisites met"
echo ""

# Stop existing container
echo "🛑 Stopping existing containers..."
docker-compose down

# Build new image
echo "🏗️  Building Docker image..."
docker-compose build --no-cache

# Start container
echo "🚀 Starting bot container..."
docker-compose up -d

# Show logs
echo ""
echo "✅ Bot deployed successfully!"
echo ""
echo "📊 Container Status:"
docker-compose ps
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop bot with: docker-compose down"
echo "🔄 Restart bot with: docker-compose restart"
echo ""
echo "🎉 Bot is now running 24/7!"