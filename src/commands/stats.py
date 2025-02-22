import os
import logging
import requests
from discord.ext import commands

# Configuration
JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

# Setup logging
logging.basicConfig(level=logging.INFO)

class StatsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(ADMIN_ROLE_ID)
    async def stats(self, ctx):
        """Displays the current number of listeners and bitrate."""
        try:
            response = requests.get(JSON_URL)
            response.raise_for_status()
            data = response.json()
            listeners = data["icestats"]["source"]["listeners"]
            bitrate = data["icestats"]["source"].get("bitrate", "N/A")

            stats_message = (
                f"📊 **Stream Stats**:\n"
                f"👂 **Current listeners**: {listeners}\n"
                f"📈 **Bitrate**: {bitrate} kbps\n"
            )
            await ctx.send(stats_message)
        except requests.RequestException as e:
            await ctx.send("Unable to fetch statistics.")
            logging.error(f"Error: {e}")

def setup(bot):
    bot.add_cog(StatsCommand(bot))