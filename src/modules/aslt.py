import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.stats import skew

class ASLT(BaseEstimator,TransformerMixin):
    '''
    Automatic Shifted Log Transform (ASLT) based on Feng et al (2016)
    '''
    def __init__(self,beta:float|list|np.ndarray=None):
        '''
        Initializes automatic log transformer

        Args:
            beta (float | list | np.ndarray): If float is used, calculate beta for each column using its skewness and multiply it by the beta argument. If list is used, beta values for each column will be taken from it (dimension of list must match the number of columns of X).  
        '''
        self.beta = beta
    
    def fit(self,X:np.ndarray,y=None):
        X = np.asarray(X, dtype=float)
        if isinstance(self.beta,(list,np.ndarray,tuple,set)):
            if len(self.beta) != X.shape[1]:
                raise IndexError('Dimension of beta and X columns does not match!')
        else:
            self.beta = skew(X,axis=0)*self.beta
        self.beta = np.where(self.beta == 0, 1e-8, self.beta)
        
        self.xmin_ = np.min(X,axis=0)
        self.xmax_ = np.max(X,axis=0)
        self.R_ = self.xmax_ - self.xmin_
        return self
    
    def transform(self,X:np.ndarray):
        return self.__autolog(X)

    def __autolog(self,X:np.ndarray):
        X = np.asarray(X, dtype=float)
        X_copy = X.copy()
        for i in range(X_copy.shape[1]):
            if self.beta[i] > 0:
                X_copy[:,i] = np.log(np.clip(X_copy[:,i] - self.xmin_[i] + self.R_[i]/np.abs(self.beta[i]),1e-8,None))
            elif self.beta[i] < 0:
                X_copy[:,i] = -np.log(np.clip(self.xmax_[i] - X_copy[:,i] + self.R_[i]/np.abs(self.beta[i]),1e-8,None))
        return X_copy