import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
from src.bot import bot

class CheckScheduledEventsTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def check_scheduled_events(self):
        guild = self.bot.guilds[0]
        events = await guild.fetch_scheduled_events()

        now = datetime.now(timezone.utc)

        for event in events:
            if event.status == discord.EventStatus.scheduled:
                time_diff = (event.start_time - now).total_seconds()

                if 0 <= time_diff <= 300:
                    try:
                        await event.start()
                        print(f"✅ L'événement {event.name} a été lancé automatiquement !")
                    except Exception as e:
                        print(f"❌ Impossible de démarrer {event.name} : {e}")

def setup(bot):
    bot.add_cog(CheckScheduledEventsTask(bot))