# Utiliser l'image Python Slim pour réduire la taille
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances en premier (pour optimiser le cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY ./app /app

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]