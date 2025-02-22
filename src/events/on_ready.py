import logging
from discord.ext import commands, tasks
from datetime import datetime, timezone
from src.tasks.update_status import update_status
from src.tasks.ensure_connected import ensure_connected
from src.tasks.check_scheduled_events import check_scheduled_events

class OnReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.get_cog("UpdateStatusTask").update_status.start()
        self.bot.get_cog("EnsureConnectedTask").ensure_connected.start()
        self.bot.get_cog("CheckScheduledEventsTask").check_scheduled_events.start()
        logging.info(f"{self.bot.user.name} is online!")

def setup(bot):
    bot.add_cog(OnReadyEvent(bot))