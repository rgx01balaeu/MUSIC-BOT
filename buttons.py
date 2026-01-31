from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("▶ Play", callback_data="cb_play"), InlineKeyboardButton("🔍 Search", callback_data="cb_search")],
        [InlineKeyboardButton("📜 Queue", callback_data="cb_queue"), InlineKeyboardButton("⏸ Pause", callback_data="cb_pause")],
        [InlineKeyboardButton("📋 Commands", callback_data="cb_commands"), InlineKeyboardButton("⚙ Settings", callback_data="cb_settings")],
        [InlineKeyboardButton("🎤 Lyrics", callback_data="cb_lyrics"), InlineKeyboardButton("❌ Close", callback_data="cb_close")]
    ])

def player_buttons(is_playing=True, song_id=None):
    play_pause_btn = InlineKeyboardButton("⏸ Pause", callback_data="cb_pause") if is_playing else InlineKeyboardButton("▶ Resume", callback_data="cb_resume")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏮ Prev", callback_data="cb_prev"), play_pause_btn, InlineKeyboardButton("⏭ Skip", callback_data="cb_skip")],
        [InlineKeyboardButton("⏪ −10m", callback_data="cb_seek_back"), InlineKeyboardButton("⏩ +10m", callback_data="cb_seek_forward")],
        [InlineKeyboardButton("🔉 Vol-", callback_data="cb_vol_down"), InlineKeyboardButton("🔊 Vol+", callback_data="cb_vol_up")],
        [InlineKeyboardButton("📜 Queue", callback_data="cb_queue"), InlineKeyboardButton("🎤 Lyrics", callback_data="cb_lyrics")],
        [InlineKeyboardButton("❤️ Like", callback_data=f"cb_like_{song_id}" if song_id else "cb_like"), InlineKeyboardButton("📀 Info", callback_data="cb_info")],
        [InlineKeyboardButton("🔁 Loop", callback_data="cb_loop"), InlineKeyboardButton("🔀 Shuffle", callback_data="cb_shuffle")],
        [InlineKeyboardButton("⏹ Stop", callback_data="cb_stop")]
    ])

def settings_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Classic", callback_data="set_theme_classic"), InlineKeyboardButton("🌙 Dark", callback_data="set_theme_dark")],
        [InlineKeyboardButton("⚡ Neon", callback_data="set_theme_neon"), InlineKeyboardButton("👑 Gold", callback_data="set_theme_gold")],
        [InlineKeyboardButton("🔙 Back", callback_data="cb_main_menu")]
    ])

def commands_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="cb_main_menu")]
    ])

def lyrics_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="cb_player")]
    ])
