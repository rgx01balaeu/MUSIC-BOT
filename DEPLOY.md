# 🚀 VPS Deployment Guide

## 1. Prepare your VPS
Recommended OS: Ubuntu 22.04 LTS

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip ffmpeg git -y
```

## 2. Deployment

### Using Screen:
```bash
screen -S musicbot
python3 -m bot.main
# Press Ctrl+A followed by D to detach
```

### Using Systemd (Recommended):
Create `/etc/systemd/system/musicbot.service`:
```ini
[Unit]
Description=Telegram Music Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/music-bot
ExecStart=/usr/bin/python3 -m bot.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable musicbot
sudo systemctl start musicbot
```

## 3. Performance Tips
- Use a VPS with at least 1GB RAM.
- Choose a region close to Telegram's data centers (e.g., Amsterdam, Frankfurt).
