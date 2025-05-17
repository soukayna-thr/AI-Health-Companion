
from flask import Blueprint, request, jsonify
from models.models import Prediction
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db

recommendation = Blueprint("recommendation", __name__)

# Base de recommandations
recommendations = {
    "Diabetes": ["Évitez le sucre", "Faites du sport", "Mangez des fibres"],
    "Anemia": ["Mangez plus de fer", "Prenez des compléments", "Consultez un médecin"],
    "Thalasse": ["Suivez un suivi médical", "Hydratez-vous bien"],
    "Thromboc": ["Évitez les aliments gras", "Prenez des anticoagulants"],
    "Heart Disease": ["Évitez le stress", "Réduisez le sel"],
    "Healthy": ["Continuez votre hygiène de vie !"]
}

# 🔹 Route pour obtenir la recommandation à partir de la maladie détectée
@recommendation.route("/recommendation", methods=["GET"])
@jwt_required(optional=True)  # Permet aux utilisateurs connectés d’avoir des recommandations basées sur leur historique
def get_recommendation():
    condition = request.args.get("condition")

    if condition in recommendations:
        return jsonify({"condition": condition, "recommendations": recommendations[condition]})

    return jsonify({"message": "Condition inconnue"}), 400

# 🔹 Route pour récupérer les dernières recommandations basées sur l'historique des prédictions
@recommendation.route("/recommendation/history", methods=["GET"])
@jwt_required()  # Uniquement pour les utilisateurs connectés
def get_recommendation_history():
    user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.timestamp.desc()).limit(5).all()

    if not predictions:
        return jsonify({"message": "Aucune prédiction trouvée"}), 404

    history = [
        {
            "condition": p.condition,
            "probability": p.probability,
            "recommendations": recommendations.get(p.condition, ["Aucune recommandation disponible"]),
            "timestamp": p.timestamp
        }
        for p in predictions
    ]

    return jsonify({"history": history})
