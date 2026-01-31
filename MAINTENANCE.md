# 🛠 Maintenance Plan

## 🔄 Regular Updates
- Keep `yt-dlp` updated to avoid YouTube download failures:
  ```bash
  pip install -U yt-dlp
  ```
- Update `pytgcalls` and `pyrogram` for new features and bug fixes.

## 🧹 Cleanup
- Periodically clear the `music_bot.db` if it grows too large (though SQLite is efficient).
- Remove any temporary files in the root directory (thumbnails, etc.).

## 📈 Monitoring
- Check `journalctl -u musicbot -f` for any crashes.
- Monitor VPS resource usage (CPU/RAM) during high load.

## 💾 Backups
- Regularly backup `music_bot.db` to prevent data loss (Favorites, Whitelist).
- Backup your `.env` or `config.py` file.
