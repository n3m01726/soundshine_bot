import os
import logging
import discord
from discord.ext import commands
from datetime import datetime
from utils.check_stream_online import check_stream_online

# Configuration
STREAM_URL = "https://stream.soundshineradio.com:8445/stream"
JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

# Setup logging
logging.basicConfig(level=logging.INFO)

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx):
        """Command to play the stream."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You should be in the voice channel below before doing the command.\n\nIl faut que tu sois dans le canal vocal ci-dessous pour pouvoir faire cette commande.\n\nLien du Canal Vocal | Link to Vocal Channel -> https://discordapp.com/channels/1292508602082525227/1324247709502406748")
            return

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client and ctx.voice_client.is_connected():
            vc = ctx.voice_client
        else:
            vc = await voice_channel.connect()

        if voice_channel.type == discord.ChannelType.stage_voice:
            try:
                await vc.channel.guild.me.edit(suppress=False)
                await ctx.send("The bot is now a speaker in the Stage Channel.")
            except discord.DiscordException as e:
                await ctx.send(f"Error promoting to speaker: {e}")

        if vc.is_playing():
            await ctx.send("The stream is already playing.")
            return

        if not await check_stream_online():
            await ctx.send("❌ Le stream est actuellement hors ligne. Veuillez réessayer plus tard.")
            current_time = datetime.now().strftime("%H:%M:%S")
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"OFFLINE since {current_time}"))
            logging.error(f"Stream is offline as of {current_time}. The bot status has been updated.")
            return

        vc.play(discord.FFmpegPCMAudio(STREAM_URL), after=lambda e: logging.info("Stream ended"))
        await ctx.send("The stream has started!")

def setup(bot):
    bot.add_cog(PlayCommand(bot))