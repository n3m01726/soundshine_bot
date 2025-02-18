import discord
from discord.ext import commands
import logging
import sys
import locale
from config import Config
from cogs.radio import RadioCog
from cogs.quiz import QuizCog

# Configure more detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('bot')  # Create a specific logger for our bot

# Configure system and locale settings
sys.stdout.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

class SoundshineBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!s",
            intents=intents
        )

    async def setup_hook(self):
        try:
            await self.add_cog(RadioCog(self))
            await self.add_cog(QuizCog(self))
            logger.info("Cogs loaded successfully")
        except Exception as e:
            logger.error(f"Error loading cogs: {e}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} ({self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds")

def main():
    bot = SoundshineBot()
    try:
        logger.info("Starting bot...")
        bot.run(Config.BOT_TOKEN, log_handler=None)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()