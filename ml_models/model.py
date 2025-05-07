from abc import abstractmethod, ABC

class Model(ABC):
    @abstractmethod
    def fit(self,X,Y): pass

    @abstractmethod
    def predict(self,X): pass