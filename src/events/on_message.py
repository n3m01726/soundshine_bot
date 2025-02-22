import discord
from discord.ext import commands
import os

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel) and message.content.lower() == "scan":
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

            if log_channel:
                await log_channel.send("--== Scan des musiques en cours ==--")
                await message.channel.send("Le message a bien été envoyé sur le serveur ! ✅")

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(OnMessageEvent(bot))