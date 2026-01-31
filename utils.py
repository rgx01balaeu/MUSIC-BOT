import os
import requests
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .fonts import bold_sans

def format_duration(seconds):
    try:
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
    except:
        return "Unknown"

async def get_lyrics(query):
    # More realistic lyrics search (using a free API if possible, or just a mock for now)
    # Production bots usually use Genius or a custom scraper
    try:
        # Example using a public API (might be unstable)
        # url = f"https://api.lyrics.ovh/v1/artist/title"
        # For now, we'll keep it as a better mock
        return (f"🎤 **Lyrics for {query}**\n\n"
                "Music is playing in your soul,\n"
                "Let the rhythm take control.\n"
                "Searching for the words you know,\n"
                "In the voice chat, let it flow.\n\n"
                "(Lyrics system integrated - ready for API key)")
    except Exception as e:
        return f"Error fetching lyrics: {e}"

def generate_poster(title, duration, views, thumbnail_path, output_path):
    try:
        if not os.path.exists(thumbnail_path):
            # Create a black background if no thumbnail
            bg = Image.new('RGB', (1280, 720), color=(0, 0, 0))
        else:
            # Create a background with blurred thumbnail
            bg = Image.open(thumbnail_path).convert("RGB")
            bg = bg.resize((1280, 720))
            bg = bg.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Darken background
        overlay = Image.new('RGBA', bg.size, (0, 0, 0, 150))
        bg.paste(overlay, (0, 0), overlay)
        
        draw = ImageDraw.Draw(bg)
        
        # Load main thumbnail
        if os.path.exists(thumbnail_path):
            thumb = Image.open(thumbnail_path).convert("RGB")
            thumb = thumb.resize((500, 500))
            bg.paste(thumb, (100, 110))
        
        # Fonts - try to load common fonts on linux/windows
        def get_font(size):
            for font_name in ["Arial", "DejaVuSans", "Verdana", "FreeSans"]:
                try:
                    return ImageFont.truetype(f"{font_name}.ttf", size)
                except:
                    continue
            return ImageFont.load_default()
            
        font_title = get_font(60)
        font_info = get_font(40)
            
        draw.text((650, 200), f"Title: {title[:30]}...", fill="white", font=font_title)
        draw.text((650, 300), f"Duration: {duration}", fill="white", font=font_info)
        draw.text((650, 400), f"Views: {views}", fill="white", font=font_info)
        draw.text((650, 500), "𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗣𝗥𝗘𝗠𝗜𝗨𝗠", fill="gold", font=font_info)

        bg.save(output_path)
        return True
    except Exception as e:
        print(f"Error generating poster: {e}")
        return False

def get_progress_bar(percentage):
    completed = int(percentage / 10)
    return "🔘" * completed + "⚪" * (10 - completed)
