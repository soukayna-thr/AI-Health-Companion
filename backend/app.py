"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from flask_jwt_extended import JWTManager

from config.config import Config
from models import db  
from models.models import User  
from dotenv import load_dotenv
import os
import openai
from routes.auth import auth
from routes.prediction import prediction
from routes.upload import upload
from routes.recommendation import recommendation
from routes.chatbot import chatbot
from routes.dashboard import dashboard


app = Flask(__name__)
app.config.from_object(Config)
load_dotenv() 
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print("📂 Chargement du fichier .env depuis :", dotenv_path)

load_dotenv(dotenv_path)  # ✅ Force le chargement du fichier .env

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ Clé API non trouvée ! Vérifiez si .env existe et est correct.")
else:
    print("✅ Clé API trouvée :", openai_api_key[:10] + "********")

openai.api_key = os.getenv("OPENAI_API_KEY")
print("✅ Clé API OpenAI chargée :", openai.api_key[:10] + "********" if openai.api_key else "❌ Clé API non trouvée !")

# 🔹 Initialisation UNIQUE de SQLAlchemy et JWT
db.init_app(app)
migrate = Migrate(app, db)  
app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

# 🔹 Enregistrement des routes
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(prediction, url_prefix="")
app.register_blueprint(upload, url_prefix="/upload")
app.register_blueprint(recommendation, url_prefix="/recommend")
app.register_blueprint(chatbot, url_prefix="/chatbot")
app.register_blueprint(dashboard, url_prefix="/dashboard")


if __name__ == "__main__":
    with app.app_context():  
        db.create_all()  # ✅ Seulement si Flask-Migrate n'est pas utilisé
    app.run(debug=True, port=5000)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import openai

from config.config import Config
from models import db  
from models.models import User  
from routes.auth import auth
from routes.prediction import prediction
from routes.upload import upload
from routes.recommendation import recommendation
from routes.chatbot import chatbot
from routes.dashboard import dashboard

# ✅ Charger les variables d’environnement depuis `.env`
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"📂 Chargement du fichier .env depuis : {dotenv_path}")
else:
    print("⚠️ Alerte : Aucun fichier .env trouvé ! Vérifiez son emplacement.")

# ✅ Charger la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("❌ Clé API OpenAI non trouvée ! Vérifiez votre variable d'environnement.")
else:
    print(f"✅ Clé API OpenAI trouvée : {openai.api_key[:10]}********")

# 🔹 Initialisation de l’application Flask
app = Flask(__name__)
app.config.from_object(Config)

# 🔹 Initialisation UNIQUE de SQLAlchemy et JWT
db.init_app(app)
migrate = Migrate(app, db)  
app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

# 🔹 Enregistrement des routes
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(prediction, url_prefix="")
app.register_blueprint(upload, url_prefix="/upload")
app.register_blueprint(recommendation, url_prefix="/recommend")
app.register_blueprint(chatbot, url_prefix="/chatbot")
app.register_blueprint(dashboard, url_prefix="/dashboard")

# 🔹 Démarrer l'application Flask
if __name__ == "__main__":
    with app.app_context():  
        db.create_all()  # ✅ Seulement si Flask-Migrate n'est pas utilisé
    app.run(debug=True, port=5000)"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from config.config import Config
from models import db  
from models.models import User  
from routes.auth import auth
from routes.prediction import prediction
from routes.upload import upload
from routes.recommendation import recommendation
from routes.chatbot import chatbot
from routes.dashboard import dashboard

# ✅ Charger les variables d’environnement depuis `.env`
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"📂 Chargement du fichier .env depuis : {dotenv_path}")
else:
    print("⚠️ Alerte : Aucun fichier .env trouvé ! Vérifiez son emplacement.")

# ✅ Charger la clé API Hugging Face
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

if not huggingface_api_key:
    print("❌ Clé API Hugging Face non trouvée ! Vérifiez votre variable d'environnement.")
else:
    print(f"✅ Clé API Hugging Face trouvée : {huggingface_api_key[:10]}********")

# 🔹 Initialisation de l’application Flask
app = Flask(__name__)
app.config.from_object(Config)

# 🔹 Initialisation UNIQUE de SQLAlchemy et JWT
db.init_app(app)
migrate = Migrate(app, db)  
app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

# 🔹 Enregistrement des routes
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(prediction, url_prefix="")
app.register_blueprint(upload, url_prefix="/upload")
app.register_blueprint(recommendation, url_prefix="/recommend")
app.register_blueprint(chatbot, url_prefix="/chatbot")  # ✅ Chatbot mis à jour pour Hugging Face
app.register_blueprint(dashboard, url_prefix="/dashboard")

# 🔹 Démarrer l'application Flask
if __name__ == "__main__":
    with app.app_context():  
        db.create_all()  # ✅ Seulement si Flask-Migrate n'est pas utilisé
    app.run(debug=True, port=5000)
