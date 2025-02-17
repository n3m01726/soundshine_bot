# -*- coding: utf-8 -*-

import os
import sys
import locale
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
import aiohttp

# Icecast Configuration
STREAM_URL = os.getenv("STREAM_URL")
JSON_URL = os.getenv("JSON_URL")
RADIO_DJ_API = os.getenv("RADIO_DJ_API")

# Discord Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))
BOT_ROLE_NAME = os.getenv("BOT_ROLE_NAME")
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

# Other Configuration
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_API")

sys.stdout.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # Adapter selon ton serveur

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create intents for permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a bot instance with intents
bot = commands.Bot(command_prefix="!s", intents=intents)

@bot.event
async def on_ready():
    ensure_connected.start()
    update_status.start()
    logging.info(f"{bot.user.name} is online!")

@tasks.loop(seconds=20)
async def update_status():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(JSON_URL, timeout=10) as response:
                response.raise_for_status()  # Vérifie si l'URL répond
                data = await response.json()

                # Vérifie que la clé 'icestats' et 'source' existent dans les données
                if "icestats" in data and "source" in data["icestats"]:
                    current_song = data["icestats"]["source"].get("title", "No title available")
                else:
                    current_song = "Stream offline or no song information available"

                # Log des chansons et mise à jour du statut Discord
                logging.info(f"Current song fetched: {current_song}")
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f": {current_song}"))

        except aiohttp.ClientError as e:
            logging.error(f"Error fetching metadata or updating status: {e}")
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Soundshine Radio"))  # Statut par défaut

@bot.command()
async def play(ctx):
    """Command to play the stream."""
    # Vérifie si l'utilisateur est dans un salon vocal
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("You should be in the voice channel below before doing the command.\n\nIl faut que tu sois dans le canal vocal ci-dessous pour pouvoir faire cette commande.\n\nLien du Canal Vocal | Link to Vocal Channel -> https://discordapp.com/channels/1292508602082525227/1324247709502406748")
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
            await ctx.send("The bot is now a speaker in the Stage Channel.")
        except discord.DiscordException as e:
            await ctx.send(f"Error promoting to speaker: {e}")

    # Vérifie si le bot joue déjà quelque chose
    if vc.is_playing():
        await ctx.send("The stream is already playing.")
        return

    # Vérification si le stream est en ligne
    if not await check_stream_online():
        await ctx.send("❌ Le stream est actuellement hors ligne. Veuillez réessayer plus tard.")
        # Mise à jour du statut du bot en "OFFLINE"
        current_time = datetime.now().strftime("%H:%M:%S")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"OFFLINE since {current_time}"))
        logging.error(f"Stream is offline as of {current_time}. The bot status has been updated.")
        return

    vc.play(discord.FFmpegPCMAudio(STREAM_URL), after=lambda e: logging.info("Stream ended"))
    await ctx.send("The stream has started!")

@bot.command()
async def join(ctx):
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


async def check_stream_online():
    """Vérifie si le stream est en ligne en récupérant les métadonnées du stream."""
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()  # Lève une exception si la réponse est une erreur
        data = response.json()
        # Si les données sont valides, on considère que le stream est en ligne
        if data["icestats"]["source"]["title"] != "":
            return True
        else:
            return False
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la vérification du stream : {e}")
        return False

@bot.command()
async def stop(ctx):
    """Command to stop the stream (only available in the #admin channel)."""
    if ctx.channel.id != int(ADMIN_CHANNEL_ID):
        await ctx.send(f"This command can only be used in the <#{ADMIN_CHANNEL_ID}> channel.")
        return

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("The stream has stopped and the bot has left the voice channel.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def np(ctx):
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

@tasks.loop(seconds=30)
async def ensure_connected():
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel and not bot.voice_clients:
        await voice_channel.connect()

@bot.command()
@commands.has_role(ADMIN_ROLE_ID)
async def stats(ctx):
    """Displays the current number of listeners."""
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()
        # Nombre d'écouteurs
        listeners = data["icestats"]["source"]["listeners"]
        
        # Débit binaire (Bitrate)
        bitrate = data["icestats"]["source"].get("bitrate", "N/A")
    
        # Construction du message
        stats_message = (
            f"📊 **Stream Stats**:\n"
            f"👂 **Current listeners**: {listeners}\n"
            f"📈 **Bitrate**: {bitrate} kbps\n"
            
        )
        await ctx.send(f"{stats_message}")
    except requests.RequestException as e:
        await ctx.send("Unable to fetch statistics.")
        logging.error(f"Error: {e}")

@bot.command()
async def schedule(ctx):
    """Affiche la programmation sous forme d'embed interactif."""
    try:
        # Lecture du fichier schedule.txt
        with open("schedule.txt", "r", encoding="utf-8") as file:
            schedule_content = file.read()

        # Séparation en anglais/français
        sections = schedule_content.split("🗓")
        en_schedule = sections[1].strip() if len(sections) > 1 else "Aucune donnée."
        fr_schedule = sections[2].strip() if len(sections) > 2 else "Aucune donnée."

        # Création des embeds
        embed_en = discord.Embed(title="📅 Schedule (EN)", description=en_schedule, color=0x3498db)
        embed_fr = discord.Embed(title="📅 Horaire (FR)", description=fr_schedule, color=0xe74c3c)

        # Création du menu déroulant
        class ScheduleDropdown(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="🇬🇧 English Schedule", value="en", emoji="🇬🇧"),
                    discord.SelectOption(label="🇫🇷 Horaire Français", value="fr", emoji="🇫🇷"),
                ]
                super().__init__(placeholder="Choisissez une langue", options=options)

            async def callback(self, interaction: discord.Interaction):
                if self.values[0] == "en":
                    await interaction.response.edit_message(embed=embed_en)
                else:
                    await interaction.response.edit_message(embed=embed_fr)

        view = View()
        view.add_item(ScheduleDropdown())

        # Envoi du message initial avec le menu
        await ctx.send(embed=embed_en, view=view)

    except Exception as e:
        await ctx.send("❌ Impossible de lire la programmation.")
        print(f"Erreur : {e}")

@bot.command()
async def getwall(ctx):
    """Commande pour récupérer une photo aléatoire de Unsplash"""
    try:
        response = requests.get(f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&count=1")
        response.raise_for_status()
        photo_data = response.json()
        photo_url = photo_data[0]["urls"]["regular"]
        await ctx.send(photo_url)
    except requests.RequestException as e:
        await ctx.send("Erreur lors de la récupération de l'image.")
        logging.error(f"Error fetching photo: {e}")

bot.run(BOT_TOKEN)
