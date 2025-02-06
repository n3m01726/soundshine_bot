# bot/commands/quiz.py

import random
import asyncio
from discord.ext import commands
import logging

# Liste de questions (ajoute-en plus si tu veux)
questions = [
    {"question": "Quel est le plus grand océan du monde ?", "choices": ["Atlantique", "Pacifique", "Indien", "Arctique"], "answer": "🇧"},
    {"question": "Qui a peint La Joconde ?", "choices": ["Michel-Ange", "Léonard de Vinci", "Raphaël", "Van Gogh"], "answer": "🇧"},
    {"question": "Combien y a-t-il de continents sur Terre ?", "choices": ["4", "5", "6", "7"], "answer": "🇩"}
]

@commands.command()
async def quiz(ctx):
    """Lance une question de quiz en format QCM."""
    question = random.choice(questions)
    choices_emojis = ["🇦", "🇧", "🇨", "🇩"]
    
    # Construire le message
    question_text = f"**{question['question']}**\n\n"
    for emoji, choice in zip(choices_emojis, question["choices"]):
        question_text += f"{emoji} {choice}\n"
    
    quiz_message = await ctx.send(question_text)
    
    # Ajouter les réactions
    for emoji in choices_emojis:
        await quiz_message.add_reaction(emoji)
    
    # Attendre 10 secondes avant de donner la réponse
    await asyncio.sleep(10)
    
    # Afficher la réponse correcte
    await ctx.send(f"✅ La bonne réponse était {question['answer']} !")
