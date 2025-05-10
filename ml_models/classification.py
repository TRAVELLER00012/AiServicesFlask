from .model import Model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import joblib

class LogisticRegressionModel(Model):
    
    @staticmethod
    def fit(X, Y, user_id):
        classifier = LogisticRegression()
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        classifier.fit(x,y)
        joblib.dump(classifier, f"./media/user_models/{user_id}_LOGISTIC.pkl")
    
    @staticmethod
    def predict(X,user_id):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        model = joblib.load(f"./media/user_models/{user_id}_LOGISTIC.pkl")
        return model.predict(x)

class DecissionTreeC(Model):
    @staticmethod
    def fit(X, Y,user_id):
        classifier = DecisionTreeClassifier()
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        classifier.fit(x,y)
        joblib.dump(classifier, f"./media/user_models/{user_id}_DTC.pkl")
    
    @staticmethod
    def predict(X,user_id):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        model = joblib.load(f"./media/user_models/{user_id}_DTC.pkl")
        return model.predict(x)