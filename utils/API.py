# bot/utils/api.py

import requests
import os
import logging

API_URL = os.getenv("API_URL")  # L'URL de l'API à interroger, par exemple : "http://localhost:5000/api"

def get_current_song():
    """Récupère la chanson actuelle depuis l'API."""
    try:
        response = requests.get(f"{API_URL}/current_song")
        response.raise_for_status()
        data = response.json()
        return data.get("song", "Aucune chanson en cours")
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération de la chanson actuelle: {e}")
        return "Erreur lors de la récupération de la chanson"

def get_last_songs(limit=5):
    """Récupère les dernières chansons jouées depuis l'API."""
    try:
        response = requests.get(f"{API_URL}/last_songs?limit={limit}")
        response.raise_for_status()
        data = response.json()
        return data.get("songs", [])
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération des dernières chansons: {e}")
        return []

def get_upcoming_songs(limit=3):
    """Récupère les prochaines chansons depuis l'API."""
    try:
        response = requests.get(f"{API_URL}/upcoming_songs?limit={limit}")
        response.raise_for_status()
        data = response.json()
        return data.get("songs", [])
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération des prochaines chansons: {e}")
        return []
