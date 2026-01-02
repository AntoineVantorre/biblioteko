FROM python:3.11-slim

# On utilise slim pour avoir une image plus légère
WORKDIR /app

# Installation des dépendances système (nécessaires pour tes bibliothèques de transcription/images)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    libsm6 \
    libxrender1 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

# 1. Copier le requirements.txt seul pour optimiser le cache Docker
COPY requirements.txt .

# 2. Installer les dépendances (C'est ici que pydantic-settings sera installé)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copier tout le code source du dossier backend vers /app
COPY . .

# 4. Lancer l'application avec le mode RELOAD pour le développement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]