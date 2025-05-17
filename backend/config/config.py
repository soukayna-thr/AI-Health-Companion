import os

class Config:
    # 🔐 Clé secrète pour sécuriser les sessions et JWT (remplace par une vraie clé en production)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    # 🔌 Configuration de la base de données SQLite (peut être changée pour MySQL ou PostgreSQL)
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"  # Utilise SQLite pour stocker les utilisateurs
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📂 Dossier où les fichiers uploadés seront stockés
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

    # 📦 Autoriser les types de fichiers valides pour l’upload
    ALLOWED_EXTENSIONS = {"csv", "pdf"}
