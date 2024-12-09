from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return access_token
    return None

@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    token = authenticate(data['email'], data['password'])
    if token:
        return jsonify(access_token=token), 200
    return jsonify({"message": "Invalid credentials"}), 401