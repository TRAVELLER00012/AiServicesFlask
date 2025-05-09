import os
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import ml_models.regression as regression
from models.models import AiModel, db

MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media" )
os.makedirs(MEDIA_FOLDER, exist_ok=True)

regression_routes = Blueprint("regression",__name__)

def fit_model(model_type,model):
    user = get_jwt_identity()
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

    existing_model = AiModel.query.filter_by(user_id=user,model_type=model_type).first()
    if not existing_model:
        new_model = AiModel(user_id=user,model_type=model_type)
        db.session.add(new_model)
        db.session.commit()
    

    X.save(X_path)
    Y.save(Y_path)
    model.fit(X.filename,Y.filename, user)
    return jsonify({"message":"File uploaded successfully"})



def predict(model_type,model):
    user = get_jwt_identity()

    if "file1" not in request.files:
        return jsonify({"error":"Specify a 'X.csv' file"}), 400
    
    X = request.files["file1"]

    if X.filename == "":
        return jsonify({"error":"'X.csv' need to be specified"}) , 400
    
    if X.mimetype != "text/csv":
        return jsonify({"error":"File must be in csv format."}), 400
    
    X_path = os.path.join(MEDIA_FOLDER, X.filename)    
    
    premade_model = AiModel.query.filter_by(user_id=user,model_type=model_type).first()
    if not premade_model:
        return jsonify({"error":"Train your model before making predictions"}), 400

    
    X.save(X_path)
    predictions = model.predict(X.filename,user)
    return jsonify(predictions.tolist())




@regression_routes.route("/linear/fit",methods=["POST"])
@jwt_required()
def train_linear():
    try:
        return fit_model("LINEAR_REG",regression.Linear)
    except:
        return jsonify({"error":"Some error occurred"}), 500

@regression_routes.route("/linear/predict",methods=["POST"])
@jwt_required()
def predict_linear():
    try:
        return predict("LINEAR_REG",regression.Linear)
    except:
        return jsonify({"error":"Some error occurred"}), 500

@regression_routes.route("/svr/fit",methods=["POST"])
@jwt_required()
def train_svr():
    kernel = request.args.get("kernel",default="rbf")
    gamma = request.args.get("gamma","auto")
    degree = int(request.args.get("degree",3))
    C = float(request.args.get("C",1.0))
    e = float(request.args.get("e",0.1))
    return fit_model("SVR_REG",regression.SVR_Model(kernel,gamma,degree,C,e))


@regression_routes.route("/svr/predict",methods=["POST"])
@jwt_required()
def predict_svr():
    try:
        return predict("SVR_REG",regression.SVR_Model)
    except:
        return jsonify({"error":"Some error occurred"}), 500
    


@regression_routes.route("/dtr/fit",methods=["POST"])
@jwt_required()
def train_dtr():
    try:
        return fit_model("DTR_REG",regression.DecisionTreeRModel)
    except:
        return jsonify({"error":"Some error occurred"}), 500
    
@regression_routes.route("/dtr/predict",methods=["POST"])
@jwt_required()
def predict_dtr():
    try:
        return predict("DTR_REG",regression.DecisionTreeRModel)
    except:
        return jsonify({"error":"Some error occurred"}), 500