from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import ml_models.regression as regression
from ml_models.model import fit_model, predict

regression_routes = Blueprint("regression",__name__)

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