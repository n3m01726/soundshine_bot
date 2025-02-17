# cogs/quiz.py
from discord.ext import commands
import random
import asyncio

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {
                "question": "What is the largest ocean in the world?",
                "choices": ["Atlantic", "Pacific", "Indian", "Arctic"],
                "answer": "🇧"
            },
            # Add more questions here
        ]

    @commands.command()
    async def quiz(self, ctx):
        question = random.choice(self.questions)
        choices_emojis = ["🇦", "🇧", "🇨", "🇩"]
        
        question_text = self._format_question(question, choices_emojis)
        quiz_message = await ctx.send(question_text)
        
        for emoji in choices_emojis:
            await quiz_message.add_reaction(emoji)
        
        await asyncio.sleep(10)
        await ctx.send(f"✅ The correct answer was {question['answer']}!")

    def _format_question(self, question, emojis):
        formatted = f"**{question['question']}**\n\n"
        for emoji, choice in zip(emojis, question['choices']):
            formatted += f"{emoji} {choice}\n"
        return formatted