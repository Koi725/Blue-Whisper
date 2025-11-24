# Blue Whisper Bot - Server Deployment Guide

## Quick Start on Server

### 1. Connect to Your Server

```bash
ssh root@your-server-ip
```

### 2. Run One-Command Setup

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/blue-whisper-bot/main/server-setup.sh | bash
```

### 3. Upload Bot Code

```bash
# On your local machine
scp -r blue-whisper-bot/ root@your-server-ip:~/
```

### 4. Deploy Bot

```bash
# On server
cd ~/blue-whisper-bot
./deploy.sh
```

## Done! Bot is running 24/7 🎉

---

## Management Commands

### Start Bot

```bash
./start.sh
```

### Stop Bot

```bash
./stop.sh
```

### Restart Bot

```bash
./restart.sh
```

### View Logs

```bash
./logs.sh
```

### Check Health

```bash
./monitor.sh
```

---

## Maintenance

### View Running Container

```bash
docker-compose ps
```

### Enter Container Shell

```bash
docker-compose exec bluewhisper-bot /bin/bash
```

### View Resource Usage

```bash
docker stats bluewhisper-ocean-bot
```

### Clean Up Old Images

```bash
docker system prune -a
```

---

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
docker-compose logs

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Check Token

```bash
# View environment variables
docker-compose exec bluewhisper-bot env | grep TELEGRAM
```

### Container Keeps Restarting

```bash
# View last crash logs
docker-compose logs --tail=100
```

---

## Automatic Restart on Server Reboot

The bot automatically restarts because of `restart: unless-stopped` in docker-compose.yml

Test it:

```bash
# Reboot server
sudo reboot

# Wait 2 minutes, then check
docker-compose ps
# Should show "Up X minutes"
```

---

## Backup & Restore

### Backup Logs

```bash
tar -czf backup-logs-$(date +%Y%m%d).tar.gz logs/
```

### Backup Configuration

```bash
tar -czf backup-config-$(date +%Y%m%d).tar.gz .env config/
```

---

## Security Checklist

- ✅ .env file is NOT in git (.gitignore)
- ✅ Bot runs as non-root user
- ✅ Resource limits configured
- ✅ Logging enabled
- ✅ Automatic restart enabled
- ✅ Health checks configured

---

## Monitoring

### Setup Cron Job for Daily Health Check

```bash
# Edit crontab
crontab -e

# Add this line (runs every day at 9 AM)
0 9 * * * cd ~/blue-whisper-bot && ./monitor.sh >> logs/health-$(date +\%Y\%m\%d).log 2>&1
```

### Setup Alerts (Optional)

Use services like:

- UptimeRobot (free, monitors if bot is down)
- Better Uptime
- Pingdom

---

## Cost Estimate

### Minimal Server ($5-10/month)

- **DigitalOcean Droplet**: $6/month (1GB RAM)
- **Linode Nanode**: $5/month (1GB RAM)
- **Vultr**: $5/month (1GB RAM)

Bot uses ~50-100MB RAM, so even smallest server works!

---

## Support

Issues? Check:

1. `./logs.sh` - View real-time logs
2. `./monitor.sh` - Check health status
3. `docker-compose ps` - Check container status

Still stuck? Contact: info@bluewhisper.om
