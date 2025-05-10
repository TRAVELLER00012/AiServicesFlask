import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from .model import Model
import joblib

class Linear(Model):
    @staticmethod
    def fit(X,Y, user_id):
        regressor = LinearRegression()
        x = pd.read_csv(f"media/{X}").values
        y = pd.read_csv(f"media/{Y}").values
        regressor.fit(x,y)
        joblib.dump(regressor, f"media/user_models/{user_id}_linear.pkl")

    @staticmethod
    def predict(X, user_id):
        x = pd.read_csv(f"media/{X}").values
        model = joblib.load(f"media/user_models/{user_id}_linear.pkl")
        predictions = model.predict(x)
        return predictions


class SVR_Model(Model):
    def __init__(self, kernel, gamma = "auto" ,degree = 3, C = 1.0, e = 0.1):
        self.regressor = SVR(kernel=kernel,gamma=gamma,degree=degree,C=C, epsilon=e)


    def fit(self,X,Y,user_id):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        self.regressor.fit(x,y)
        joblib.dump(self.regressor,f"media/user_models/{user_id}_SVR.pkl")
        
    @staticmethod    
    def predict(X,user_id):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        model = joblib.load(f"media/user_models/{user_id}_SVR.pkl")
        predictions = model.predict(x).reshape(-1,1)
        return predictions
    

class DecisionTreeRModel(Model):
    @staticmethod
    def fit(X,Y,user_id):
        regressor = DecisionTreeRegressor()
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        regressor.fit(x,y)
        joblib.dump(regressor,f"media/user_models/{user_id}_DTR.pkl")
        
    @staticmethod
    def predict(X,user_id):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        model = joblib.load(f"media/user_models/{user_id}_DTR.pkl")
        return model.predict(x)
