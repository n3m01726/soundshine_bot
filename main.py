# main.py
import discord
from discord.ext import commands
import logging
import sys
import locale
from config import Config
from cogs.radio import RadioCog
from cogs.quiz import QuizCog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
        await self.add_cog(RadioCog(self))
        await self.add_cog(QuizCog(self))

    async def on_ready(self):
        logging.info(f"{self.user.name} is online!")

def main():
    bot = SoundshineBot()
    bot.run(Config.BOT_TOKEN)

if __name__ == "__main__":
    main()