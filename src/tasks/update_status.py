import os
import logging
import aiohttp
import discord
from discord.ext import commands, tasks

# Load environment variables
JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"

# Setup logging
logging.basicConfig(level=logging.INFO)

class UpdateStatusTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=60)
    async def update_status(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(JSON_URL, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if "icestats" in data and "source" in data["icestats"]:
                        current_song = data["icestats"]["source"].get("title", "No title available")
                    else:
                        current_song = "Stream offline or no song information available"

                    logging.info(f"Current song fetched: {current_song}")
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=f"🎧 {current_song}"))

            except aiohttp.ClientError as e:
                logging.error(f"Error fetching metadata or updating status: {e}")
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Soundshine Radio"))

def setup(bot):
    bot.add_cog(UpdateStatusTask(bot))