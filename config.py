import os

API_ID = int(os.getenv("API_ID", "35432101"))
API_HASH = os.getenv("API_HASH", "16ec3bc04171468c2d89ac798dde60d2")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8545544711:AAGtFuPYpqzzIdByXIY9kWrcwpaBw5l5KYE")
OWNER_ID = int(os.getenv("OWNER_ID", "8306405497"))

DB_NAME = "music_bot.db"
SESSION_NAME = "music_bot"
ASSISTANT_SESSION = os.getenv("ASSISTANT_SESSION", "")

# Themes
THEMES = {
    "classic": "🎧",
    "dark": "🌙",
    "neon": "⚡",
    "gold": "👑"
}
