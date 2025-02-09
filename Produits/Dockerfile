# Utilisation d'une image Python légère
FROM python:3.12-slim

# Définition du répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers nécessaires
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet
COPY . .

# Générer le client Prisma
RUN prisma generate

# Exposer le port de FastAPI
EXPOSE 8002

# Démarrer FastAPI
CMD ["sh", "-c", "python consumer.py & uvicorn main:app --host 0.0.0.0 --port 8002"]
