from .model import Model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import joblib
import os

IS_PRODUCTION = os.environ.get("RENDER", None) is not None

if IS_PRODUCTION:
    BASE_MEDIA_PATH = "/tmp"
else:
    BASE_MEDIA_PATH = os.path.join(os.getcwd(), "media")

MODEL_DIR = os.path.join(BASE_MEDIA_PATH, "user_models")
os.makedirs(MODEL_DIR, exist_ok=True)

class LogisticRegressionModel(Model):
    
    @staticmethod
    def fit(X, Y, user_id):
        classifier = LogisticRegression()
        x = pd.read_csv(X).values
        y = pd.read_csv(Y).values.ravel()  # flatten y
        classifier.fit(x, y)
        joblib.dump(classifier, f"{MODEL_DIR}/{user_id}_LOGISTIC.pkl")
    
    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(X).values
        model = joblib.load(f"{MODEL_DIR}/{user_id}_LOGISTIC.pkl")
        return model.predict(x)

class DecissionTreeC(Model):
    @staticmethod
    def fit(X, Y, user_id):
        classifier = DecisionTreeClassifier()
        x = pd.read_csv(X).values
        y = pd.read_csv(Y).values.ravel()
        classifier.fit(x, y)
        joblib.dump(classifier, f"{MODEL_DIR}/{user_id}_DTC.pkl")
    
    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(X).values
        model = joblib.load(f"{MODEL_DIR}/{user_id}_DTC.pkl")
        return model.predict(x)
