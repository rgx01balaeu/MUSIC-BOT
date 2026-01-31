import aiosqlite
from .config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS whitelist (user_id INTEGER PRIMARY KEY)")
        await db.execute("CREATE TABLE IF NOT EXISTS favorites (user_id INTEGER, song_id TEXT, title TEXT, PRIMARY KEY (user_id, song_id))")
        await db.execute("CREATE TABLE IF NOT EXISTS user_settings (user_id INTEGER PRIMARY KEY, theme TEXT DEFAULT 'classic')")
        await db.commit()

async def add_to_whitelist(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO whitelist (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def remove_from_whitelist(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM whitelist WHERE user_id = ?", (user_id,))
        await db.commit()

async def is_whitelisted(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM whitelist WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone() is not None

async def add_favorite(user_id, song_id, title):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO favorites (user_id, song_id, title) VALUES (?, ?, ?)", (user_id, song_id, title))
        await db.commit()

async def remove_favorite(user_id, song_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM favorites WHERE user_id = ? AND song_id = ?", (user_id, song_id))
        await db.commit()

async def get_favorites(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT song_id, title FROM favorites WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()

async def set_theme(user_id, theme):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO user_settings (user_id, theme) VALUES (?, ?)", (user_id, theme))
        await db.commit()

async def get_theme(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT theme FROM user_settings WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "classic"
