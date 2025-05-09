from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import ml_models.classification as classification
from ml_models.model import fit_model, predict

classification_routes = Blueprint("classification",__name__)

@classification_routes.route("/logisitic/fit",methods=["POST"])
@jwt_required()
def train_logisitc():   
    try:
        return fit_model("LOGISTIC_CLA",classification.LogisticRegressionModel)
    except:
        return jsonify({"error":"Some error occurred"}), 500

@classification_routes.route("/logisitic/predict",methods=["POST"])
@jwt_required()
def predict_logistic():
    try:
        return predict("LOGISTIC_CLA",classification.LogisticRegressionModel)
    except:
        return jsonify({"error":"Some error occurred"}), 500



@classification_routes.route("/dtc/fit",methods=["POST"])
@jwt_required()
def train_dtc():   
    try:
        return fit_model("DTC_CLA",classification.DecissionTreeC)
    except:
        return jsonify({"error":"Some error occurred"}), 500

@classification_routes.route("/dtc/predict",methods=["POST"])
@jwt_required()
def predict_dtc():
    try:
        return predict("DTC_CLA",classification.DecissionTreeC)
    except:
        return jsonify({"error":"Some error occurred"}), 500