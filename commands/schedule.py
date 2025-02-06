# bot/commands/schedule.py

import discord
from discord.ext import commands
from discord.ui import View, Select
import logging

# Commande pour afficher la programmation sous forme d'embed interactif
@commands.command()
async def schedule(ctx):
    """Affiche la programmation sous forme d'embed interactif."""
    try:
        # Lecture du fichier schedule.txt
        with open("schedule.txt", "r", encoding="utf-8") as file:
            schedule_content = file.read()

        # Séparation en anglais/français
        sections = schedule_content.split("🗓")
        en_schedule = sections[1].strip() if len(sections) > 1 else "Aucune donnée."
        fr_schedule = sections[2].strip() if len(sections) > 2 else "Aucune donnée."

        # Création des embeds
        embed_en = discord.Embed(title="📅 Schedule (EN)", description=en_schedule, color=0x3498db)
        embed_fr = discord.Embed(title="📅 Horaire (FR)", description=fr_schedule, color=0xe74c3c)

        # Création du menu déroulant
        class ScheduleDropdown(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="🇬🇧 English Schedule", value="en", emoji="🇬🇧"),
                    discord.SelectOption(label="🇫🇷 Horaire Français", value="fr", emoji="🇫🇷"),
                ]
                super().__init__(placeholder="Choisissez une langue", options=options)

            async def callback(self, interaction: discord.Interaction):
                if self.values[0] == "en":
                    await interaction.response.edit_message(embed=embed_en)
                else:
                    await interaction.response.edit_message(embed=embed_fr)

        view = View()
        view.add_item(ScheduleDropdown())

        # Envoi du message initial avec le menu
        await ctx.send(embed=embed_en, view=view)

    except Exception as e:
        await ctx.send("❌ Impossible de lire la programmation.")
        logging.error(f"Erreur lors de la lecture de la programmation : {e}")
