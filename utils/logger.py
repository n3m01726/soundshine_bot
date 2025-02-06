# bot/utils/logger.py

import logging

# Configuration du logger
def setup_logger():
    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.DEBUG)
    
    # Création d'un handler pour afficher les logs dans la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Création d'un format de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Ajout du handler au logger
    logger.addHandler(console_handler)
    
    return logger

# Exemple d'utilisation
logger = setup_logger()

def log_error(message):
    """Log une erreur."""
    logger.error(message)

def log_info(message):
    """Log une info."""
    logger.info(message)

def log_warning(message):
    """Log un avertissement."""
    logger.warning(message)
