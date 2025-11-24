#!/bin/bash
echo "🚀 Starting Blue Whisper Bot..."
docker-compose up -d
echo "✅ Bot started!"
docker-compose logs -f