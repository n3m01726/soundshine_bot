import discord
from discord.ext import commands

class JoinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Command to make the bot join the voice channel of the user."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("⚠️ You need to be in a voice channel for me to join!")
            return

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.send("🔊 I'm already connected to a voice channel.")
        else:
            await voice_channel.connect()
            await ctx.send(f"✅ Connected to {voice_channel.name}!")

def setup(bot):
    bot.add_cog(JoinCommand(bot))