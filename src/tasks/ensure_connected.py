import discord
from discord.ext import commands, tasks
import os
from soundshine_bot.src.bot import bot

VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

class EnsureConnectedTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def ensure_connected(self):
        voice_channel = self.bot.get_channel(VOICE_CHANNEL_ID)
        if voice_channel and not self.bot.voice_clients:
            await voice_channel.connect()

def setup(bot):
    bot.add_cog(EnsureConnectedTask(bot))