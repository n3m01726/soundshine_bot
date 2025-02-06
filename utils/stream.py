# bot/utils/stream.py

import requests
import logging

def get_stream_stats(api_url):
    """Récupère les statistiques du stream."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        listeners = data["icestats"]["source"]["listeners"]
        bitrate = data["icestats"]["source"].get("bitrate", "N/A")
        return listeners, bitrate
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération des stats du stream: {e}")
        return None, None
