# bot/commands/music.py

import discord
from discord.ext import commands
import logging
import requests
from datetime import datetime
from bot.utils.stream import check_stream_online

STREAM_URL = "http://soundshineradio.com:3496/stream"
JSON_URL = "http://soundshineradio.com:3496/status-json.xsl"
ADMIN_CHANNEL_NAME = "bot-crap"

# Commande pour jouer le stream
@commands.command()
async def play(ctx):
    """Command to play the stream."""
    # Vérifie si l'utilisateur est dans un salon vocal
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Tu dois être dans un salon vocal pour utiliser cette commande.")
        return

    voice_channel = ctx.author.voice.channel

    # Vérifie si le bot est déjà connecté à un salon vocal
    if ctx.voice_client and ctx.voice_client.is_connected():
        vc = ctx.voice_client
    else:
        vc = await voice_channel.connect()

    # Vérifie si le salon est un Stage Channel et tente de promouvoir le bot en Speaker
    if voice_channel.type == discord.ChannelType.stage_voice:
        try:
            await vc.channel.guild.me.edit(suppress=False)
            await ctx.send("Le bot est maintenant un speaker dans le Stage Channel.")
        except discord.DiscordException as e:
            await ctx.send(f"Erreur lors de la promotion du bot en speaker : {e}")

    # Vérifie si le bot joue déjà quelque chose
    if vc.is_playing():
        await ctx.send("Le stream est déjà en cours.")
        return

    # Vérification si le stream est en ligne
    if not await check_stream_online():
        await ctx.send("❌ Le stream est actuellement hors ligne. Veuillez réessayer plus tard.")
        # Mise à jour du statut du bot en "OFFLINE"
        current_time = datetime.now().strftime("%H:%M:%S")
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"OFFLINE since {current_time}"))
        logging.error(f"Stream is offline as of {current_time}. The bot status has been updated.")
        return

    # Lance le stream
    vc.play(discord.FFmpegPCMAudio(STREAM_URL), after=lambda e: logging.info("Stream ended"))
    await ctx.send("Le stream a démarré !")

# Commande pour rejoindre un canal vocal
@commands.command()
async def join(ctx):
    """Command to make the bot join the voice channel of the user."""
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("⚠️ Tu dois être dans un canal vocal pour que je puisse te rejoindre !")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client and ctx.voice_client.is_connected():
        await ctx.send("🔊 Je suis déjà connecté à un salon vocal.")
    else:
        await voice_channel.connect()
        await ctx.send(f"✅ Connecté à {voice_channel.name} !")

# Commande pour afficher la musique en cours
@commands.command()
async def np(ctx):
    """Displays the current song."""
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()
        current_song = data["icestats"]["source"]["title"]
        await ctx.send(f"🎶 Actuellement en train de jouer : **{current_song}**")
    except requests.RequestException as e:
        await ctx.send("Impossible de récupérer la chanson en cours.")
        logging.error(f"Error: {e}")
