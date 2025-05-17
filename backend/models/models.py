from models import db  # ✅ Utilisation de db depuis models/__init__.py
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # 🔹 Hachage du mot de passe avant stockage
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    # 🔹 Vérification du mot de passe
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Prediction(db.Model):
    __tablename__ = "prediction"
    __table_args__ = {"extend_existing": True}  # 🔹 Évite la redéfinition

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    condition = db.Column(db.String(50), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(10), nullable=False)  # "manual" ou "csv/pdf"
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
