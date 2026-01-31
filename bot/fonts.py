def bold_sans(text: str) -> str:
    res = ""
    for char in text:
        if 'A' <= char <= 'Z':
            res += chr(ord(char) - ord('A') + 0x1D5D4)
        elif 'a' <= char <= 'z':
            res += chr(ord(char) - ord('a') + 0x1D5EE)
        elif '0' <= char <= '9':
            res += chr(ord(char) - ord('0') + 0x1D7EC)
        else:
            res += char
    return res

# Mandatory styles
NOW_PLAYING_TEXT = bold_sans("NOW PLAYING")
QUEUE_TEXT = bold_sans("QUEUE")
PAUSED_TEXT = bold_sans("PAUSED")
STOPPED_TEXT = bold_sans("STOPPED")
SEARCHING_TEXT = bold_sans("SEARCHING")
WELCOME_TEXT = bold_sans("WELCOME TO MUSIC BOT")
SETTINGS_TEXT = bold_sans("SETTINGS")
COMMANDS_TEXT = bold_sans("ALL COMMANDS")
