# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
import sys
import locale

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
ADMIN_ROLE = "🛠️ Admin"

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create intents for permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a bot instance with intents
bot = commands.Bot(command_prefix="!s", intents=intents)

# Load commands and events
bot.load_extension("commands.play")
bot.load_extension("commands.join")
bot.load_extension("commands.stop")
bot.load_extension("commands.np")
bot.load_extension("commands.stats")
bot.load_extension("commands.schedule")
bot.load_extension("commands.getwall")
bot.load_extension("commands.quiz")
bot.load_extension("events.on_ready")
bot.load_extension("events.on_message")
bot.load_extension("tasks.update_status")
bot.load_extension("tasks.ensure_connected")
bot.load_extension("tasks.check_scheduled_events")

sys.stdout.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # Adapter selon ton serveur

bot.run(BOT_TOKEN)