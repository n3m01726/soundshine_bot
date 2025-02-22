import os
import requests
import logging
from discord.ext import commands

JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"

class NowPlayingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def np(self, ctx):
        """Displays the current song."""
        try:
            response = requests.get(JSON_URL)
            response.raise_for_status()
            data = response.json()
            current_song = data["icestats"]["source"]["title"]
            await ctx.send(f"🎶 Now playing: **{current_song}**")
        except requests.RequestException as e:
            await ctx.send("Unable to fetch the current song.")
            logging.error(f"Error: {e}")

def setup(bot):
    bot.add_cog(NowPlayingCommand(bot))