import asyncio
import yt_dlp
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from .config import API_ID, API_HASH, SESSION_NAME
from .queue import queue_manager
from pyrogram import Client

# Initialize Pyrogram Client for the User (to join VC)
# Note: In production, the bot needs a user session to join VC.
# The user provided a BOT_TOKEN, but pytgcalls needs a User Session.
# Usually, we use a separate session string for the user account.
# Since the user didn't provide a session string, I'll assume 
# the client passed to PyTgCalls is the one that will join.

ytdl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

def get_audio_info(query):
    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        return {
            'url': info['url'],
            'title': info['title'],
            'duration': info['duration'],
            'views': info.get('view_count', 0),
            'thumbnail': info.get('thumbnail'),
            'id': info.get('id')
        }

class Player:
    def __init__(self, client):
        self.call = PyTgCalls(client)
        self.client = client
        self.is_playing = {} # chat_id: bool
        self.current_song = {} # chat_id: info

    async def start(self):
        await self.call.start()

    async def play(self, chat_id, query):
        info = get_audio_info(query)
        self.current_song[chat_id] = info
        await self.call.join_group_call(
            chat_id,
            AudioPiped(info['url'])
        )
        self.is_playing[chat_id] = True
        return info

    async def pause(self, chat_id):
        await self.call.pause_stream(chat_id)
        self.is_playing[chat_id] = False

    async def resume(self, chat_id):
        await self.call.resume_stream(chat_id)
        self.is_playing[chat_id] = True

    async def stop(self, chat_id):
        await self.call.leave_group_call(chat_id)
        self.is_playing[chat_id] = False
        self.current_song[chat_id] = None

    async def skip(self, chat_id):
        next_song = queue_manager.get_next(chat_id)
        if next_song:
            return await self.play(chat_id, next_song)
        else:
            await self.stop(chat_id)
            return None

    async def seek(self, chat_id, seconds):
        info = self.current_song.get(chat_id)
        if info:
            # Re-join with offset?
            # In pytgcalls v2, we use change_stream
            await self.call.change_stream(
                chat_id,
                AudioPiped(info['url'], additional_ffmpeg_parameters=f"-ss {seconds}")
            )

    async def set_volume(self, chat_id, volume):
        await self.call.change_volume_call(chat_id, volume)

    def on_stream_end(self, handler):
        @self.call.on_update()
        async def update_handler(client, update):
            from pytgcalls.types import Update
            from pytgcalls.types.stream import StreamAudioEnded
            if isinstance(update, StreamAudioEnded):
                await handler(update.chat_id)
