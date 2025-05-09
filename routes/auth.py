from datetime import timedelta
from flask import Blueprint, request, jsonify,make_response
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from models.models import User

auth_routes = Blueprint("auth",__name__)

bcrypt = Bcrypt() 

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    if user is None: return jsonify({"error":"Invalid Email or Password"}), 404

    if not bcrypt.check_password_hash(user.password,data["password"]): return jsonify({"error":"Invalid Email or Password"}), 404

    response = make_response(jsonify({
        "email":user.email,
        "full_name":user.full_name,
    }))

    access_token = create_access_token(identity=str(user.id),additional_claims={"email":user.email,"id":user.id},expires_delta=timedelta(days=90))
    response.headers["Authorization"] = f"Bearer {access_token}"
    
    return response
