# bot/commands/unsplash.py

import os
import requests
from discord.ext import commands
import logging

# Récupérer la clé API Unsplash
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_API")

@commands.command()
async def getwall(ctx):
    """Commande pour récupérer une photo aléatoire de Unsplash"""
    try:
        response = requests.get(f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&count=1")
        response.raise_for_status()
        photo_data = response.json()
        photo_url = photo_data[0]["urls"]["regular"]
        await ctx.send(photo_url)
    except requests.RequestException as e:
        await ctx.send("Erreur lors de la récupération de l'image.")
        logging.error(f"Error fetching photo: {e}")
