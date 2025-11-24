#!/bin/bash

# Complete Server Setup Script for Blue Whisper Bot
# Run this on your fresh server

echo "🌊 Blue Whisper Ocean Club - Server Setup"
echo "=========================================="
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
echo "📦 Installing Git..."
sudo apt install -y git

# Create app directory
echo "📁 Creating application directory..."
mkdir -p ~/blue-whisper-bot
cd ~/blue-whisper-bot

echo ""
echo "✅ Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Upload your bot code to this directory"
echo "2. Create .env file with your token"
echo "3. Run: ./deploy.sh"
echo ""