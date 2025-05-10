from abc import abstractmethod, ABC
import os
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.models import AiModel, db


MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media" )
os.makedirs(MEDIA_FOLDER, exist_ok=True)

class Model(ABC):
    @abstractmethod
    def fit(self,X,Y): pass

    @abstractmethod
    def predict(self,X): pass


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