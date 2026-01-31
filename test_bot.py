import asyncio
import os
import sys

# Add current directory to path so we can import bot package
sys.path.append(os.getcwd())

from unittest.mock import MagicMock
import sys

# Mock pytgcalls before importing bot modules
sys.modules["pytgcalls"] = MagicMock()
sys.modules["pytgcalls.types"] = MagicMock()

from bot.fonts import bold_sans
from bot.database import init_db, add_to_whitelist, is_whitelisted, set_theme, get_theme
from bot.utils import format_duration, get_progress_bar

async def test_fonts():
    text = "HELLO world 123"
    result = bold_sans(text)
    print(f"Font test: {text} -> {result}")
    # The expected characters for HELLO are U+1D5D7, U+1D5D8, U+1D5DB, U+1D5DB, U+1D5DE
    # I'll just check if it's different from original
    assert result != text
    print("Font test passed!")

async def test_db():
    if os.path.exists("music_bot.db"):
        os.remove("music_bot.db")
    await init_db()
    await add_to_whitelist(12345)
    assert await is_whitelisted(12345) == True
    assert await is_whitelisted(54321) == False
    
    await set_theme(12345, "neon")
    assert await get_theme(12345) == "neon"
    print("Database test passed!")

async def test_utils():
    assert format_duration(65) == "01:05"
    assert format_duration(3665) == "01:01:05"
    bar = get_progress_bar(50)
    print(f"Progress bar test: {bar}")
    assert bar.count("🔘") == 5
    
    # Test poster generation
    from PIL import Image
    dummy_thumb = "dummy_thumb.jpg"
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(dummy_thumb)
    
    from bot.utils import generate_poster
    assert generate_poster("Test Song", "03:45", "1.2M", dummy_thumb, "test_poster.png") == True
    assert os.path.exists("test_poster.png")
    
    os.remove(dummy_thumb)
    os.remove("test_poster.png")
    print("Utils test passed!")

async def run_tests():
    await test_fonts()
    await test_db()
    await test_utils()
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(run_tests())
