import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from .model import Model
import joblib
import os

IS_PRODUCTION = os.environ.get("RENDER", None) is not None

if IS_PRODUCTION:
    BASE_MEDIA_PATH = "/tmp"
else:
    BASE_MEDIA_PATH = os.path.join(os.getcwd(), "media")

MODEL_DIR = os.path.join(BASE_MEDIA_PATH, "user_models")
os.makedirs(MODEL_DIR, exist_ok=True)
class Linear(Model):
    @staticmethod
    def fit(X, Y, user_id):
        regressor = LinearRegression()
        x = pd.read_csv(X).values
        y = pd.read_csv(Y).values.ravel()
        regressor.fit(x, y)
        joblib.dump(regressor, f"{MODEL_DIR}/{user_id}_linear.pkl")

    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(X).values
        model = joblib.load(f"{MODEL_DIR}/{user_id}_linear.pkl")
        return model.predict(x)


class SVR_Model(Model):
    def __init__(self, kernel="rbf", gamma="auto", degree=3, C=1.0, e=0.1):
        self.regressor = SVR(kernel=kernel, gamma=gamma, degree=degree, C=C, epsilon=e)

    def fit(self, X, Y, user_id):
        x = pd.read_csv(X).values
        y = pd.read_csv(Y).values.ravel()
        self.regressor.fit(x, y)
        joblib.dump(self.regressor, f"{MODEL_DIR}/{user_id}_SVR.pkl")

    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(X).values
        model = joblib.load(f"{MODEL_DIR}/{user_id}_SVR.pkl")
        return model.predict(x).reshape(-1, 1)


class DecisionTreeRModel(Model):
    @staticmethod
    def fit(X, Y, user_id):
        regressor = DecisionTreeRegressor()
        x = pd.read_csv(X).values
        y = pd.read_csv(Y).values.ravel()
        regressor.fit(x, y)
        joblib.dump(regressor, f"{MODEL_DIR}/{user_id}_DTR.pkl")

    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(X).values
        model = joblib.load(f"{MODEL_DIR}/{user_id}_DTR.pkl")
        return model.predict(x)
