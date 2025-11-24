#!/bin/bash

# Bot Health Monitoring Script

echo "🏥 Blue Whisper Bot - Health Monitor"
echo "===================================="
echo ""

# Check if container is running
if [ "$(docker-compose ps -q bluewhisper-bot)" ]; then
    echo "✅ Container Status: RUNNING"
    
    # Get container stats
    echo ""
    echo "📊 Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" bluewhisper-bot
    
    # Show uptime
    echo ""
    echo "⏰ Container Uptime:"
    docker-compose ps
    
    # Show recent logs
    echo ""
    echo "📝 Recent Logs (last 20 lines):"
    docker-compose logs --tail=20
    
else
    echo "❌ Container Status: NOT RUNNING"
    echo ""
    echo "Start the bot with: ./start.sh"
fi

echo ""
echo "===================================="