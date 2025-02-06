# bot/bot.py

import logging
import discord
from discord.ext import commands, tasks
from .config import BOT_TOKEN, ADMIN_CHANNEL_NAME
from .utils.logger import setup_logger

# Configuration du logger
setup_logger()

# Création de l'instance du bot avec les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!s", intents=intents)

@bot.event
async def on_ready():
    """Événement appelé lorsque le bot est prêt."""
    logging.info(f"{bot.user.name} est en ligne et prêt à fonctionner !")
    ensure_connected.start()
    update_status.start()

@tasks.loop(seconds=20)
async def update_status():
    """Met à jour le statut du bot (par exemple, la chanson en cours)."""
    # Logique de mise à jour du statut (voir la partie update_status de la première section)
    pass

@tasks.loop(seconds=30)
async def ensure_connected():
    """Vérifie régulièrement si le bot est connecté à un canal vocal."""
    # Logique pour garantir que le bot reste connecté à un canal vocal
    pass

# Chargement des extensions (commands)
bot.load_extension("bot.commands.music")
bot.load_extension("bot.commands.schedule")
bot.load_extension("bot.commands.quiz")
bot.load_extension("bot.commands.admin")
bot.load_extension("bot.commands.unsplash")

# Exécution du bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
