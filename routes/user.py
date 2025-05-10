from datetime import timedelta
from flask import Blueprint,request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from models.models import db, User, UserSchema

user_routes = Blueprint("users",__name__)
bcrypt = Bcrypt()
user_schema = UserSchema()

@user_routes.route("/register",methods=["POST"])
def register():
    data = request.get_json()

    try:
        validated_data = user_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    
    user = User(
        full_name = data["full_name"],
        password = hashed_password,
        email = data["email"]
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "1062" in str(e.orig): return jsonify("Email is already in use.") ,400
        else: return jsonify(str(e))
    except Exception as e:
        return jsonify(str(e))

    response = make_response(jsonify({
        "full_name":data["full_name"],
        "email":data["email"]
    }))
    response.headers["Authorization"] = f"Bearer {create_access_token(identity=str(user), additional_claims={'email':data['email']}, expires_delta=timedelta(days=90))}"
    return response
