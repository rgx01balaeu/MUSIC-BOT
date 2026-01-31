import asyncio
import os
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import Message, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from .config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, ASSISTANT_SESSION
from .database import init_db, add_to_whitelist, remove_from_whitelist, is_whitelisted, get_theme, set_theme, add_favorite, get_favorites
from .buttons import main_menu_buttons, player_buttons, settings_buttons, commands_buttons, lyrics_buttons
from .fonts import *
from .player import Player, get_audio_info
from .queue import queue_manager
from .utils import generate_poster, format_duration, get_progress_bar, get_lyrics
from .auth import is_authorized, is_owner

# Initialize Clients
bot = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

assistant = None
if ASSISTANT_SESSION:
    assistant = Client(
        "music_assistant",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=ASSISTANT_SESSION
    )

player = Player(assistant if assistant else bot)

# Chat states
chat_volume = {} # chat_id: int (0-200)

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    if not await is_authorized(message.from_user.id):
        return await message.reply_text("❌ You are not authorized to use this bot.")
    
    await message.reply_text(
        f"🎧 {WELCOME_TEXT}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "✨ High Quality VC Music\n"
        "⚡ Fast Streaming\n"
        "🔐 Private Access\n"
        "🎶 YouTube & Web Search",
        reply_markup=main_menu_buttons()
    )

async def play_song(chat_id, query, message=None):
    try:
        # Non-blocking info fetch
        info = await asyncio.to_thread(get_audio_info, query)
        
        # Download thumbnail for poster
        thumb_path = f"thumb_{info['id']}.jpg"
        if info['thumbnail']:
            r = await asyncio.to_thread(requests.get, info['thumbnail'])
            with open(thumb_path, 'wb') as f:
                f.write(r.content)
        
        poster_path = f"poster_{info['id']}.png"
        await asyncio.to_thread(generate_poster, info['title'], format_duration(info['duration']), info['views'], thumb_path, poster_path)
        
        await player.play(chat_id, query)
        
        caption = (f"🎧 {NOW_PLAYING_TEXT}\n\n"
                   f"🎵 **Title:** {info['title']}\n"
                   f"⏱ **Duration:** {format_duration(info['duration'])}\n"
                   f"👁 **Views:** {info['views']}\n\n"
                   f"{get_progress_bar(0)}\n")
        
        if message:
            await message.reply_photo(
                photo=poster_path,
                caption=caption,
                reply_markup=player_buttons(True, info['id'])
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo=poster_path,
                caption=caption,
                reply_markup=player_buttons(True, info['id'])
            )
        
        # Cleanup
        if os.path.exists(thumb_path): os.remove(thumb_path)
        if os.path.exists(poster_path): os.remove(poster_path)
        
        return info
    except Exception as e:
        if message: await message.reply_text(f"❌ Error: {str(e)}")
        print(f"Play Error: {e}")

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(client, message):
    if not await is_authorized(message.from_user.id):
        return await message.reply_text("❌ Not authorized.")
    
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("❌ Please provide a song name or URL.")
    
    m = await message.reply_text(f"🔍 {SEARCHING_TEXT}...")
    
    chat_id = message.chat.id
    if chat_id in player.is_playing and player.is_playing[chat_id]:
        # Just get info to show what's added
        info = await asyncio.to_thread(get_audio_info, query)
        queue_manager.add(chat_id, query)
        await m.edit_text(f"➕ Added to {QUEUE_TEXT}: {info['title']}")
    else:
        await m.delete()
        await play_song(chat_id, query, message)

async def next_song_handler(chat_id):
    next_query = queue_manager.get_next(chat_id)
    if next_query:
        await play_song(chat_id, next_query)
    else:
        player.is_playing[chat_id] = False
        await bot.send_message(chat_id, f"⏹ {STOPPED_TEXT}")

player.on_stream_end(next_song_handler)

@bot.on_callback_query(filters.regex("^cb_"))
async def cb_handler(client, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    data = cb.data
    
    if data == "cb_pause":
        await player.pause(chat_id)
        await cb.answer("Paused ⏸")
        await cb.message.edit_reply_markup(player_buttons(False))
        
    elif data == "cb_resume":
        await player.resume(chat_id)
        await cb.answer("Resumed ▶")
        await cb.message.edit_reply_markup(player_buttons(True))
        
    elif data == "cb_stop":
        await player.stop(chat_id)
        queue_manager.clear(chat_id)
        await cb.answer("Stopped ⏹")
        await cb.message.edit_text(f"⏹ {STOPPED_TEXT}")
        
    elif data == "cb_skip":
        await cb.answer("Skipping... ⏭")
        await player.stop(chat_id)
        await next_song_handler(chat_id)
        await cb.message.delete()

    elif data == "cb_vol_up":
        vol = chat_volume.get(chat_id, 100)
        vol = min(vol + 10, 200)
        chat_volume[chat_id] = vol
        await player.set_volume(chat_id, vol)
        await cb.answer(f"Volume: {vol}%")

    elif data == "cb_vol_down":
        vol = chat_volume.get(chat_id, 100)
        vol = max(vol - 10, 0)
        chat_volume[chat_id] = vol
        await player.set_volume(chat_id, vol)
        await cb.answer(f"Volume: {vol}%")

    elif data == "cb_loop":
        is_loop = queue_manager.toggle_loop(chat_id)
        await cb.answer(f"Loop {'Enabled 🔁' if is_loop else 'Disabled ➡️'}")

    elif data == "cb_shuffle":
        queue_manager.shuffle(chat_id)
        await cb.answer("Queue Shuffled 🔀")

    elif data.startswith("cb_like_"):
        song_id = data.split("_")[-1]
        # In a real case we'd need the title too, maybe fetch from current_song
        title = player.current_song.get(chat_id, {}).get('title', 'Unknown')
        await add_favorite(cb.from_user.id, song_id, title)
        await cb.answer(f"❤️ Added to favorites!")

    elif data == "cb_info":
        info = player.current_song.get(chat_id)
        if info:
            await cb.answer(f"🎵 {info['title']}\n👁 {info['views']} views", show_alert=True)
        else:
            await cb.answer("No info available.")

    elif data == "cb_queue":
        q = queue_manager.get_queue(chat_id)
        if not q:
            await cb.answer("Queue is empty.", show_alert=True)
        else:
            text = f"📜 {QUEUE_TEXT}\n\n"
            for i, query in enumerate(q[:10], 1):
                text += f"{i}. {query}\n"
            await cb.message.reply_text(text)
            await cb.answer()

    elif data == "cb_settings":
        await cb.message.edit_text(f"⚙ {SETTINGS_TEXT}", reply_markup=settings_buttons())

    elif data == "cb_main_menu":
        await cb.message.edit_text(
            f"🎧 {WELCOME_TEXT}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✨ High Quality VC Music\n"
            "⚡ Fast Streaming\n"
            "🔐 Private Access\n"
            "🎶 YouTube & Web Search",
            reply_markup=main_menu_buttons()
        )

    elif data.startswith("set_theme_"):
        theme = data.split("_")[-1]
        await set_theme(cb.from_user.id, theme)
        await cb.answer(f"Theme set to {theme.capitalize()}!")
        await cb.message.edit_text(f"⚙ {SETTINGS_TEXT}\n\nCurrent Theme: {theme.capitalize()}", reply_markup=settings_buttons())

    elif data == "cb_close":
        await cb.message.delete()

    elif data == "cb_lyrics":
        query = None
        if chat_id in player.current_song and player.current_song[chat_id]:
            query = player.current_song[chat_id]['title']
        if query:
            lyrics = await get_lyrics(query)
            await cb.message.edit_text(f"🎤 **Lyrics for {query}**\n\n{lyrics[:4000]}", reply_markup=lyrics_buttons())
        else:
            await cb.answer("❌ Nothing playing to get lyrics for.", show_alert=True)

@bot.on_message(filters.command(["fav", "like"]))
async def like_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    chat_id = message.chat.id
    if chat_id in player.current_song and player.current_song[chat_id]:
        song = player.current_song[chat_id]
        await add_favorite(message.from_user.id, song['id'], song['title'])
        await message.reply_text(f"❤️ Added to favorites: {song['title']}")
    else:
        await message.reply_text("❌ Nothing playing.")

@bot.on_message(filters.command("lyrics"))
async def lyrics_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    query = " ".join(message.command[1:])
    if not query and message.chat.id in player.current_song and player.current_song[message.chat.id]:
        query = player.current_song[message.chat.id]['title']
    
    if not query:
        return await message.reply_text("❌ Provide a song name for lyrics.")
        
    m = await message.reply_text("🎤 Searching lyrics...")
    lyrics = await get_lyrics(query)
    await m.edit_text(f"🎤 **Lyrics for {query}**\n\n{lyrics[:4000]}", reply_markup=lyrics_buttons())

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    await message.reply_text(
        f"📋 {COMMANDS_TEXT}\n\n"
        "**/play** <song> - Play music\n"
        "**/pause** - Pause music\n"
        "**/resume** - Resume music\n"
        "**/skip** - Skip current song\n"
        "**/stop** - Stop music\n"
        "**/queue** - Show queue\n"
        "**/lyrics** - Get lyrics\n"
        "**/fav** - Like current song\n"
        "**/adduser** <id> - Whitelist user (Owner)\n"
        "**/deluser** <id> - Remove from whitelist (Owner)\n"
        "**/help** - Show this message",
        reply_markup=commands_buttons()
    )

@bot.on_message(filters.command("adduser") & filters.user(OWNER_ID))
async def add_user_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /adduser <user_id>")
    user_id = int(message.command[1])
    await add_to_whitelist(user_id)
    await message.reply_text(f"✅ User {user_id} added to whitelist.")

@bot.on_message(filters.command("deluser") & filters.user(OWNER_ID))
async def del_user_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /deluser <user_id>")
    user_id = int(message.command[1])
    await remove_from_whitelist(user_id)
    await message.reply_text(f"✅ User {user_id} removed from whitelist.")

async def main():
    await init_db()
    await bot.start()
    if assistant:
        await assistant.start()
    await player.start()
    print("Bot started!")
    await idle()
    await bot.stop()
    if assistant:
        await assistant.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
