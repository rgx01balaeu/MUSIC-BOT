# 🎧 Telegram VC Music Bot - Installation Guide

## 🛠 Prerequisites

- Python 3.9 or higher
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to PATH
- Telegram API ID and Hash (get from [my.telegram.org](https://my.telegram.org))
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- A Telegram account to act as the Assistant (required for Voice Chat joining)

## 📥 Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd music-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   Edit `bot/config.py` or set environment variables:
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `BOT_TOKEN`: Your Bot Token
   - `OWNER_ID`: Your Telegram User ID
   - `ASSISTANT_SESSION`: Your Assistant Session String (see below)

4. **Generate Assistant Session String:**
   You can use a simple script to generate this:
   ```python
   from pyrogram import Client
   api_id = 12345
   api_hash = "your_hash"
   with Client(":memory:", api_id, api_hash) as app:
       print(app.export_session_string())
   ```
   Copy the output to `ASSISTANT_SESSION`.

5. **Run the bot:**
   ```bash
   python -m bot.main
   ```

## 🐳 Docker (Optional)

If you prefer using Docker:
```bash
docker build -t music-bot .
docker run -e API_ID=... -e API_HASH=... -e BOT_TOKEN=... music-bot
```
