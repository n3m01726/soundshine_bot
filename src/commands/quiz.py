import random
import discord
from discord.ext import commands

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {"question": "Quel est le plus grand océan du monde ?", "choices": ["Atlantique", "Pacifique", "Indien", "Arctique"], "answer": "🇧"},
            {"question": "Qui a peint La Joconde ?", "choices": ["Michel-Ange", "Léonard de Vinci", "Raphaël", "Van Gogh"], "answer": "🇧"},
            {"question": "Combien y a-t-il de continents sur Terre ?", "choices": ["4", "5", "6", "7"], "answer": "🇩"}
        ]

    @commands.command()
    async def quiz(self, ctx):
        question = random.choice(self.questions)
        choices_emojis = ["🇦", "🇧", "🇨", "🇩"]
        
        question_text = f"**{question['question']}**\n\n"
        for emoji, choice in zip(choices_emojis, question["choices"]):
            question_text += f"{emoji} {choice}\n"
        
        quiz_message = await ctx.send(question_text)
        
        for emoji in choices_emojis:
            await quiz_message.add_reaction(emoji)
        
        await asyncio.sleep(10)
        
        await ctx.send(f"✅ La bonne réponse était {question['answer']} !")

def setup(bot):
    bot.add_cog(Quiz(bot))