import requests
import os
import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv

# ✅ Charger les variables d'environnement depuis `.env`
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# ✅ Vérifier que la clé API est bien chargée
if not HUGGINGFACE_API_KEY:
    print("❌ Clé API Hugging Face non trouvée ! Vérifiez votre .env.")
else:
    print(f"✅ Clé API Hugging Face trouvée : {HUGGINGFACE_API_KEY[:10]}********")

# ✅ Définition du modèle Hugging Face (Zephyr-7B-Alpha)
MODEL_NAME = "HuggingFaceH4/zephyr-7b-alpha"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

# ✅ Vérifier si le modèle est chargé
def wait_for_model():
    """
    Vérifie si le modèle est prêt avant de démarrer Flask.
    Attend jusqu'à ce que le modèle soit chargé.
    """
    while True:
        response = requests.get(API_URL, headers=HEADERS)

        if response.status_code == 200:
            print(f"✅ Modèle '{MODEL_NAME}' chargé, prêt à l'utilisation !")
            return True
        else:
            error_details = response.json()
            print(f"⏳ Modèle en cours de chargement... Vérification dans 10 secondes.")
            time.sleep(10)

# ✅ Attendre que le modèle soit chargé avant de démarrer Flask
wait_for_model()

# ✅ Créer un Blueprint Flask pour le chatbot
chatbot = Blueprint("chatbot", __name__)

# ✅ Vérifier si le modèle est prêt via API Flask
@chatbot.route("/check_model", methods=["GET"])
def check_model():
    """
    Vérifie si le modèle Zephyr-7B-Alpha est chargé sur Hugging Face.
    """
    try:
        response = requests.get(API_URL, headers=HEADERS)

        if response.status_code == 200:
            return jsonify({"status": "success", "message": f"Modèle '{MODEL_NAME}' bien chargé !"}), 200
        else:
            return jsonify({"status": "error", "message": "Le modèle est en cours de chargement ou indisponible.", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ✅ Fonction pour envoyer une question à Zephyr-7B-Alpha
def ask_medical_question(question):
    """
    Envoie une question au modèle Zephyr-7B-Alpha via l'API Hugging Face et retourne la réponse.
    """
    payload = {
        "inputs": question,
        "parameters": {
            "max_length": 500,  # 🔹 Augmente la longueur des réponses
            "temperature": 0.7,  # 🔹 Rend la réponse plus naturelle
            "top_p": 0.9,  # 🔹 Contrôle la diversité des réponses
            "do_sample": True  # 🔹 Active la variabilité des réponses
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            error_details = response.json()
            print(f"❌ Erreur API Hugging Face : {error_details}")
            return f"❌ Erreur API Hugging Face : {error_details}"

        return response.json()[0]["generated_text"].strip()  # 🔹 Nettoyer la réponse

    except Exception as e:
        return f"❌ Erreur API : {str(e)}"


# ✅ Route Flask pour le chatbot
@chatbot.route("/chat", methods=["POST"])
@jwt_required(optional=True)
def chat():
    print(f"📩 Données brutes reçues : {request.data}")
    print(f"📩 Type Content-Type : {request.content_type}")

    try:
        # 🔹 Vérifier si le JSON reçu est valide
        data = request.get_json(silent=True)
        if not data or "message" not in data:
            return jsonify({"error": "JSON invalide. Assurez-vous d'envoyer un champ 'message'."}), 400

        user_input = data["message"]
        print(f"📨 Question posée : {user_input}")

        # 🔹 Appel au modèle Hugging Face pour obtenir une réponse
        chatbot_response = ask_medical_question(user_input)

        print(f"📩 Réponse du chatbot : {chatbot_response}")
        return jsonify({"response": chatbot_response})

    except Exception as e:
        print(f"❌ Erreur API : {str(e)}")
        return jsonify({"error": str(e)}), 500
