# bot/commands/admin.py

from discord.ext import commands
import logging

@commands.command()
async def stop(ctx):
    """Command to stop the stream (only available in the #admin channel)."""
    if ctx.channel.name != "admin":  # Change to your actual admin channel name
        await ctx.send(f"This command can only be used in the #admin channel.")
        return

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("The stream has stopped and the bot has left the voice channel.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@commands.command()
async def stats(ctx):
    """Displays the current number of listeners."""
    try:
        response = requests.get("https://api.example.com/stream_stats")  # Replace with your stream API
        response.raise_for_status()
        data = response.json()
        listeners = data["icestats"]["source"]["listeners"]
        bitrate = data["icestats"]["source"].get("bitrate", "N/A")
    
        stats_message = (
            f"📊 **Stream Stats**:\n"
            f"👂 **Current listeners**: {listeners}\n"
            f"📈 **Bitrate**: {bitrate} kbps\n"
        )
        await ctx.send(f"{stats_message}")
    except requests.RequestException as e:
        await ctx.send("Unable to fetch statistics.")
        logging.error(f"Error: {e}")
