# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    STREAM_URL = "https://stream.soundshineradio.com:8445/stream"
    JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    VOICE_CHANNEL_ID = 1324247709502406748
    ADMIN_CHANNEL_NAME = "bot-crap"
    BOT_ROLE_NAME = "soundSHINE Radio"
    ADMIN_ROLE = "🛠️ Admin"
    UNSPLASH_API_KEY = os.getenv("UNSPLASH_API")
    LOG_CHANNEL_ID = 1292526077281046600