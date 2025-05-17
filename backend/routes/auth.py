from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.models import User

auth = Blueprint("auth", __name__)  

@auth.route("/test-auth", methods=["GET"])
def test_auth():
    return {"message": "Auth route is working!"}

# 🔹 Route d'inscription
@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Nom d'utilisateur et mot de passe requis"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Utilisateur déjà existant"}), 400

    new_user = User(username=username)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Inscription réussie"}), 201 

# 🔹 Route de connexion
@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Nom d'utilisateur et mot de passe requis"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)  
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect"}), 401 

# 🔹 Route protégée par JWT
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Bienvenue {current_user} !"}), 200
