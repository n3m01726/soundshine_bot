import os
import requests
import logging

JSON_URL = "https://stream.soundshineradio.com:8445/status-json.xsl"

async def check_stream_online():
    """Vérifie si le stream est en ligne en récupérant les métadonnées du stream."""
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()
        if data["icestats"]["source"]["title"] != "":
            return True
        else:
            return False
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la vérification du stream : {e}")
        return False