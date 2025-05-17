"""import os
import pandas as pd
import pdfplumber
import pickle
import numpy as np
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.models import Prediction

prediction = Blueprint("prediction", __name__)

UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {"csv", "pdf"}

MODEL_MANUAL_PATH = "backend/models/models_manu.pkl"  # 📌 Modèle pour la saisie manuelle (9 inputs)
MODEL_CSV_PATH = "backend/models/models_file.pkl"  # 📌 Modèle pour les fichiers CSV/PDF (24 inputs)

# 🔹 Charger un modèle spécifique
def load_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    return None

model_manual = load_model(MODEL_MANUAL_PATH)  # Modèle pour la saisie manuelle
model_csv = load_model(MODEL_CSV_PATH)  # Modèle pour les fichiers

# 🔹 Liste des maladies
disease_labels = ["Diabetes", "Anemia", "Thalasse", "Thromboc", "Heart Disease", "Healthy"]

# 🔹 Vérifier si le fichier est valide
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@prediction.route("/predict/manual", methods=["POST"])
@jwt_required(optional=True)  
def predict_manual():
    if not model_manual:
        return jsonify({"message": "Modèle manuel non chargé"}), 500

    data = request.json
    input_data = np.array([
        [data["glucose"], data["cholesterol"], data["blood_pressure"],
         data["bmi"], data["age"], data["ldl"], data["hdl"], data["alt"], data["ast"]]
    ])
    
    probabilities = model_manual.predict_proba(input_data)[0]
    disease_detected = disease_labels[np.argmax(probabilities)]  
    probability_detected = max(probabilities)

    user_id = get_jwt_identity()
    new_prediction = Prediction(
        user_id=user_id, 
        condition=disease_detected, 
        probability=probability_detected, 
        source="manual"
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        "probabilities": dict(zip(disease_labels, probabilities)),
        "predicted_condition": disease_detected,
        "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
    }), 200

@prediction.route("/predict/csv", methods=["POST"])
@jwt_required(optional=True)
def predict_csv():
    if not model_csv:
        return jsonify({"message": "Modèle CSV non chargé"}), 500

    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)
    probabilities = model_csv.predict_proba(df.values)  

    predictions = []
    user_id = get_jwt_identity()

    for i, row in df.iterrows():
        disease_detected = disease_labels[np.argmax(probabilities[i])]
        probability_detected = max(probabilities[i])

        new_prediction = Prediction(
            user_id=user_id, 
            condition=disease_detected, 
            probability=probability_detected, 
            source="csv"
        )
        db.session.add(new_prediction)

        predictions.append({
            "id": i,
            "predicted_condition": disease_detected,
            "probabilities": dict(zip(disease_labels, probabilities[i])),
            "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
        })

    db.session.commit()

    return jsonify({
        "message": "Prédictions effectuées",
        "predictions": predictions
    }), 200

@prediction.route("/predict/pdf", methods=["POST"])
@jwt_required(optional=True)
def predict_pdf():
    if not model_csv:
        return jsonify({"message": "Modèle PDF non chargé"}), 500

    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    file = request.files["file"]
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    extracted_values = [float(value) for value in text.split() if value.replace('.', '', 1).isdigit()]
    
    if len(extracted_values) < 24:
        return jsonify({"message": "Données insuffisantes extraites du PDF"}), 400

    input_data = np.array([extracted_values[:24]])  
    probabilities = model_csv.predict_proba(input_data)[0]

    disease_detected = disease_labels[np.argmax(probabilities)]
    probability_detected = max(probabilities)

    user_id = get_jwt_identity()
    new_prediction = Prediction(
        user_id=user_id, 
        condition=disease_detected, 
        probability=probability_detected, 
        source="pdf"
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        "probabilities": dict(zip(disease_labels, probabilities)),
        "predicted_condition": disease_detected,
        "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
    }), 200"""

import os
import pandas as pd
import pdfplumber
import pickle
import numpy as np
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.models import Prediction, db

prediction = Blueprint("prediction", __name__)

# 📌 Modèles de prédiction
MODEL_MANUAL_PATH = "backend/models/models_manu.pkl"  # 🔹 Modèle manuel (9 inputs)
MODEL_CSV_PATH = "backend/models/models_file.pkl"  # 🔹 Modèle CSV/PDF (24 inputs)
import os

print("📂 Vérification des fichiers modèles...")
print(f"📂 Fichier manuel : {os.path.exists('backend/models/models_manu.pkl')}")
print(f"📂 Fichier CSV : {os.path.exists('backend/models/models_file.pkl')}")


# 🔹 Charger un modèle spécifique
def load_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

model_manual = load_model(MODEL_MANUAL_PATH)
model_csv = load_model(MODEL_CSV_PATH)

if not model_manual or not model_csv:
    print("❌ Erreur : Un des modèles n'a pas été trouvé ! Vérifiez les fichiers .pkl.")
else:
    print("✅ Modèles chargés avec succès !")

# 🔹 Liste des maladies
disease_labels = ["Diabetes", "Anemia", "Thalasse", "Thromboc", "Heart Disease", "Healthy"]

@prediction.route("/predict/manual", methods=["POST"])
@jwt_required(optional=True)
def predict_manual():
    if not model_manual:
        return jsonify({"message": "Modèle manuel non chargé"}), 500

    data = request.json
    input_data = np.array([[
        data["glucose"], data["cholesterol"], data["blood_pressure"],
        data["bmi"], data["age"], data["ldl"], data["hdl"], data["alt"], data["ast"]
    ]])
    
    probabilities = model_manual.predict_proba(input_data)[0]
    disease_detected = disease_labels[np.argmax(probabilities)]  
    probability_detected = max(probabilities)

    user_id = get_jwt_identity()
    new_prediction = Prediction(
        user_id=user_id, 
        condition=disease_detected, 
        probability=probability_detected, 
        source="manual"
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        "probabilities": dict(zip(disease_labels, probabilities)),
        "predicted_condition": disease_detected,
        "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
    }), 200

@prediction.route("/predict/csv", methods=["POST"])
@jwt_required(optional=True)
def predict_csv():
    if not model_csv:
        return jsonify({"message": "Modèle CSV non chargé"}), 500

    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)
    probabilities = model_csv.predict_proba(df.values)  

    predictions = []
    user_id = get_jwt_identity()

    for i, row in df.iterrows():
        disease_detected = disease_labels[np.argmax(probabilities[i])]
        probability_detected = max(probabilities[i])

        new_prediction = Prediction(
            user_id=user_id, 
            condition=disease_detected, 
            probability=probability_detected, 
            source="csv"
        )
        db.session.add(new_prediction)

        predictions.append({
            "id": i,
            "predicted_condition": disease_detected,
            "probabilities": dict(zip(disease_labels, probabilities[i])),
            "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
        })

    db.session.commit()

    return jsonify({
        "message": "Prédictions effectuées",
        "predictions": predictions
    }), 200

@prediction.route("/predict/pdf", methods=["POST"])
@jwt_required(optional=True)
def predict_pdf():
    if not model_csv:
        return jsonify({"message": "Modèle PDF non chargé"}), 500

    if "file" not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    file = request.files["file"]
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    extracted_values = [float(value) for value in text.split() if value.replace('.', '', 1).isdigit()]
    
    if len(extracted_values) < 24:
        return jsonify({"message": "Données insuffisantes extraites du PDF"}), 400

    input_data = np.array([extracted_values[:24]])  
    probabilities = model_csv.predict_proba(input_data)[0]

    disease_detected = disease_labels[np.argmax(probabilities)]
    probability_detected = max(probabilities)

    user_id = get_jwt_identity()
    new_prediction = Prediction(
        user_id=user_id, 
        condition=disease_detected, 
        probability=probability_detected, 
        source="pdf"
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        "probabilities": dict(zip(disease_labels, probabilities)),
        "predicted_condition": disease_detected,
        "recommendation_url": f"http://127.0.0.1:5000/recommendation?condition={disease_detected}"
    }), 200
