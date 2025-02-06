# 🎵 soundSHINE Bot - Installation & Démarrage  

Ce bot Discord permet d'interagir avec la radio soundSHINE et d'autres fonctionnalités comme le quiz, les rôles et plus encore.

---

## 📌 **Installation & Configuration**  

### 1️⃣ **Prérequis**  
Avant de commencer, assure-toi d'avoir :  
- Un serveur sous **Linux (Debian/Ubuntu recommandé)**  
- **Python 3.11+** installé  
- **Git** installé  
- **screen** installé (optionnel mais recommandé)  
- Un bot Discord enregistré avec son **token**  

---

### 2️⃣ **Installation du bot**  

#### 📥 **Cloner le dépôt Git**  
```bash
git clone https://github.com/n3m01726/soundshine_bot.git soundshine-bot
cd soundshine_bot
```

#### 🏗️ **Créer et activer un environnement virtuel**  
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 📦 **Installer les dépendances**  
```bash
pip install -r requirements.txt
```

---

### 3️⃣ **Configuration**  

#### 🛠️ **Créer le fichier `.env`**  
Dans le dossier du bot, crée un fichier `.env` pour stocker les informations sensibles :  
```bash
nano .env
```
Ajoute les variables suivantes (exemple) :  
```ini
DISCORD_TOKEN=ton_token_ici
ICECAST_URL=http://tonserveur:port
ICECAST_USER=admin
ICECAST_PASS=motdepasse
```
**Enregistre et ferme** (CTRL + X → Y → Entrée).  

---

### 4️⃣ **Démarrage du bot**  

#### ▶️ **Démarrer avec screen (recommandé pour le garder en arrière-plan)**  
```bash
screen -S soundshine_bot
source venv/bin/activate
python botfile.py
```
Pour détacher le screen et laisser le bot tourner en arrière-plan :  
```bash
CTRL + A puis D
```

Pour revenir au screen :  
```bash
screen -r soundshine_bot
```

#### 🚀 **Démarrer sans screen (si tu veux juste tester)**  
```bash
source venv/bin/activate
python botfile.py
```
---

### 5️⃣ **Mise à jour du bot**  

Si des mises à jour sont disponibles sur le repo :  
```bash
cd soundshine_bot
git pull
source venv/bin/activate
pip install -r requirements.txt  # Réinstaller les nouvelles dépendances si nécessaire
```


### 📖 Commandes du bot

| Commandes   | Description   | Roles   |
|-------------|-------------|-------------|
| `!sstop`  | Arrête la musique  | [ ADMIN ]  |
| `!sstats`  | Affiche les statistiques de la radio  | [ ADMIN ]  | 
| `!splay`  | Joue la radio soundSHINE  | [ USER ]  |
| `!squiz`  | Démarre un quiz général  | [ USER ]  |
| `!sgetwall` | Récupère un wallpaper aléatoire depuis unsplash  | [ USER ]  |
| `!sgetwall` | Récupère un wallpaper aléatoire depuis unsplash  | [ USER ]  |
| `!sschedule` | Affiche l'horaire  | [ USER ]  |




