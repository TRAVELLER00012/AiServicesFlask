import os
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
import ml_models.regression as regression

MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media" )
os.makedirs(MEDIA_FOLDER, exist_ok=True)

regression_routes = Blueprint("regression",__name__)

linear_model = regression.Linear()

@regression_routes.route("/linear/fit",methods=["POST"])
@jwt_required()
def train_linear():
    
    if 'file1' not in request.files or "file2" not in request.files:
        return jsonify({"error":"Both 'X.csv' and 'Y.csv' need to be specified"}), 400

    X = request.files["file1"]
    Y = request.files["file2"]

    if X.filename == "" or Y.filename == "":
        return jsonify({"error":"Both 'X.csv' and 'Y.csv' need to be specified"}) , 400
    
    if X.mimetype != "text/csv" or Y.mimetype != "text/csv":
        return jsonify({"error":"Files must be in csv format."}), 400

    X_path = os.path.join(MEDIA_FOLDER, X.filename)    
    Y_path = os.path.join(MEDIA_FOLDER, Y.filename)    
    
    X.save(X_path)
    Y.save(Y_path)

    linear_model.fit(X.filename,Y.filename)

    

    return jsonify({"message":"File uploaded successfully"})