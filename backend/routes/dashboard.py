from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Prediction
from models import db

dashboard = Blueprint("dashboard", __name__)

# 🔹 Route pour récupérer toutes les prédictions de l'utilisateur connecté
@dashboard.route("/dashboard", methods=["GET"])
@jwt_required()  # Uniquement pour les utilisateurs connectés
def get_dashboard():
    user_id = get_jwt_identity()
    source = request.args.get("source", None)  # Optionnel : Filtrer par source (manual, csv, pdf)

    query = Prediction.query.filter_by(user_id=user_id)
    if source:
        query = query.filter_by(source=source)

    predictions = query.order_by(Prediction.timestamp.desc()).all()

    if not predictions:
        return jsonify({"message": "Aucune prédiction trouvée"}), 404

    return jsonify([
        {
            "id": p.id,
            "condition": p.condition,
            "probability": p.probability,
            "source": p.source,
            "timestamp": p.timestamp
        }
        for p in predictions
    ])

# 🔹 Route pour obtenir un résumé des prédictions sous forme de statistiques
@dashboard.route("/dashboard/stats", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=user_id).all()

    if not predictions:
        return jsonify({"message": "Aucune donnée trouvée"}), 404

    stats = {}
    for p in predictions:
        stats[p.condition] = stats.get(p.condition, 0) + 1

    return jsonify({"statistics": stats})
