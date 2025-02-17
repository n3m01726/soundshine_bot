# cogs/radio.py
import discord
from discord.ext import commands, tasks
from datetime import datetime
from utils import StreamUtils
from config import Config

class RadioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(seconds=60)
    async def update_status(self):
        current_song = await StreamUtils.get_current_song()
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f": {current_song}"
            )
        )

    @commands.command()
    async def play(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        if not await StreamUtils.check_stream_online():
            await ctx.send("❌ Stream is currently offline. Please try again later.")
            return

        try:
            vc = await self._connect_to_voice(ctx)
            if vc:
                vc.play(
                    discord.FFmpegPCMAudio(Config.STREAM_URL),
                    after=lambda e: logging.info("Stream ended")
                )
                await ctx.send("Stream started successfully!")
        except Exception as e:
            await ctx.send(f"Error starting stream: {e}")

    async def _connect_to_voice(self, ctx):
        """Helper method to handle voice connection logic."""
        if ctx.voice_client:
            return ctx.voice_client
        
        return await ctx.author.voice.channel.connect()