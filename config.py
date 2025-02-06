# bot/config.py

import os

# Configuration de l'API Unsplash
UNSPLASH_API = os.getenv("UNSPLASH_API", "votre_clé_unsplash")

# Configuration pour l'API RadioDJ (si applicable)
RADIO_DJ_API = os.getenv("RADIO_DJ_API", "http://localhost:5000/api")

# Autres configurations
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Paramètres du serveur de streaming (par exemple Icecast)
STREAM_API_URL = os.getenv("STREAM_API_URL", "http://localhost:8000/api")

# Paramètres pour la gestion des rôles et permissions (si besoin)
ADMIN_ROLE_ID = os.getenv("ADMIN_ROLE_ID", "1234567890")
DJ_ROLE_ID = os.getenv("DJ_ROLE_ID", "1234567890")

# Autres configurations selon les besoins...
