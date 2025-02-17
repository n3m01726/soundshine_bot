# utils.py
import logging
import aiohttp
import requests
from config import Config

class StreamUtils:
    @staticmethod
    async def check_stream_online():
        """Check if the stream is online by fetching stream metadata."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(Config.JSON_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return bool(data["icestats"]["source"]["title"])
            return False
        except Exception as e:
            logging.error(f"Error checking stream status: {e}")
            return False

    @staticmethod
    async def get_current_song():
        """Fetch current playing song from the stream."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(Config.JSON_URL) as response:
                    data = await response.json()
                    return data["icestats"]["source"]["title"]
        except Exception as e:
            logging.error(f"Error fetching current song: {e}")
            return "Unable to fetch current song"