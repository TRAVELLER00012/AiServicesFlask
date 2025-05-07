from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pandas as pd

from model import Model

class LogisticRegressionModel(Model):
    def __init__(self):
        super().__init__()
        self.regressor = LogisticRegression()
        self.x_scaler = StandardScaler()
    
    def fit(self, X, Y):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        x = self.x_scaler.fit_transform(x)
        self.regressor.fit(x,y)
    
    def predict(self, X):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        x = self.x_scaler.transform(x)
        return self.regressor.predict(x)

class DecissionTreeC(Model):
    def __init__(self):
        super().__init__()
        self.regressor = DecisionTreeClassifier()
    
    def fit(self, X, Y):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        y = pd.read_csv(f"media/{Y}").iloc[:,:].values
        self.regressor.fit(x,y)
    
    def predict(self, X):
        x = pd.read_csv(f"media/{X}").iloc[:,:].values
        return self.regressor.predict(x)


model = DecissionTreeC()
x = pd.read_csv("media/x.csv").iloc[:,:].values
y = pd.read_csv("media/y.csv").iloc[:,:].values
model.fit("x.csv","y.csv")
predictions = model.predict("x.csv")

print(predictions)
print(accuracy_score(y,predictions))