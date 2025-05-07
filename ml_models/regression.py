import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from model import Model

class Linear(Model):
    def __init__(self):
        self.regressor = LinearRegression()
    
    def fit(self,X,Y):
        x = pd.read_csv(f"media/{X}").values
        y = pd.read_csv(f"media/{Y}").values
        self.regressor.fit(x,y)

    def predict(self,X):
        x = pd.read_csv(f"media/{X}").values
        predictions = self.regressor.predict(x)
        return predictions


class SVR_Model(Model):
    def __init__(self, kernel, gamma = "auto",feature_scaling = True ,degree = 3, C = 1.0, e = 0.1):
        self.regressor = SVR(kernel=kernel,gamma=gamma,degree=degree,C=C, epsilon=e)
        self.feature_scaling = feature_scaling
        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

    
    def fit(self,X,Y):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        if self.feature_scaling:
            y = y.reshape(len(y),1)
            x =  self.x_scaler.fit_transform(x)
            y =  self.y_scaler.fit_transform(y)
        self.regressor.fit(x,y)
        
    
    def predict(self,X):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        if self.feature_scaling: x = self.x_scaler.transform(x)
        predictions = self.regressor.predict(x).reshape(-1,1)
        if self.feature_scaling:
            return self.y_scaler.inverse_transform(predictions)
        return predictions
    

class DecisionTreeRModel(DecisionTreeRegressor):
    def __init__(self, *, criterion = "squared_error", splitter = "best", max_depth = None, min_samples_split = 2, min_samples_leaf = 1, min_weight_fraction_leaf = 0, max_features = None, random_state = None, max_leaf_nodes = None, min_impurity_decrease = 0, ccp_alpha = 0):
        super().__init__(criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, random_state=random_state, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, ccp_alpha=ccp_alpha)
    
    def fit_(self,X,Y):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        self.fit(x,y)
    
    def predict_(self,X):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        return self.predict(x)
