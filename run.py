# bot/run.py

import os
import discord
from discord.ext import commands
from bot import bot  # Importation de l'instance de bot depuis bot.py
from bot.config import DEBUG_MODE
from bot.utils.logger import setup_logger

# Création du logger
logger = setup_logger()

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Chargement des extensions (modules de commande)
extensions = [
    "bot.commands.music",
    "bot.commands.schedule",
    "bot.commands.quiz",
    "bot.commands.unsplash",
    "bot.commands.admin",
]

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            logger.info(f"Extension {extension} chargée avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de l'extension {extension}: {e}")

    # Démarrage du bot
    bot.run(os.getenv("DISCORD_TOKEN"))
