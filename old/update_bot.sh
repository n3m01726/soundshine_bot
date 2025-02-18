#!/bin/bash

echo "🔄 Updating the bot..."
git pull

if [ $? -eq 0 ]; then
    echo "✅ Update successful. Restarting the bot..."

    # Arrête l'ancienne session screen
    screen -S soundshine-bot -X quit

    # Démarre une nouvelle session screen
    
    
    bash -c "screen -S soundshine-bot  && python3 -m venv vsdrbotenv && source vbotenv/bin/activate && python3 bot_s2o3u4n5d6SHINERadio.py"

    echo "🚀 Bot restarted successfully."
else
    echo "❌ Update failed. Please check for errors."
fi
