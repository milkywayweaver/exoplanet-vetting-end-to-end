from sklearn.base import BaseEstimator,TransformerMixin
import numpy as np
from  dataclasses import dataclass,asdict
import json

class OutlierRemoval(BaseEstimator,TransformerMixin):
    '''
    Outlier removal module.
    '''
    def __init__(self,iqr_boundary:float=1.5,print_detail:bool=False):
        '''
        Initializes outlier removal module using IQR method.
        Note: Order matters! Keep same column order on both train and test set to prevent removal errors.

        Args:
            iqr_boundary (float): IQR boundary value to use
            print_detail (bool): Whether to print count of removed rows or not
        Returns:
            None
        '''
        self.iqr_boundary = iqr_boundary
        self.print_detail = print_detail

        self.state = OutlierRemovalState()

    def fit(self,X_and_y):
        X,y = X_and_y
        X = np.asarray(X,dtype=np.float32)
        median = np.nanmedian(X,axis=0)
        q3 = np.nanpercentile(X,75,axis=0)
        q1 = np.nanpercentile(X,25,axis=0)
        iqr = q3 - q1

        self.lower_ = median - self.iqr_boundary*iqr
        self.upper_ = median + self.iqr_boundary*iqr

        self.state.iqr_boundary = float(self.iqr_boundary)
        self.state.lower_ = [float(low) for low in self.lower_]
        self.state.upper_ = [float(up) for up in self.upper_]

        return self

    def transform(self,X_and_y):
        X,y = X_and_y
        X = np.asarray(X,dtype=np.float32)
        outlier_mask = (X < self.lower_) | (X > self.upper_)
        any_outlier = outlier_mask.any(axis=1)

        X_new = X[~any_outlier]
        y_new = y[~any_outlier]
        if self.print_detail:
            print(f'Removed {any_outlier.sum()} rows during outlier removal')
        return (X_new,y_new)

    def save_state_dict(self,file_path):
        '''
        Saves state dict into a JSON file.

        Args:
            file_path (str): Path where the JSON file will be saved.
        Returns:
            None 
        '''
        self.state.save(file_path=file_path)

    def load_state_dict(self,file_path):
        '''
        Loads a JSON state dict into self.

        Args:
            file_path (str): Path to the JSON file containing the state dict.
        Returns:
            None 
        '''
        self.state.load(file_path=file_path)

@dataclass
class OutlierRemovalState:
    iqr_boundary:float | None = None
    lower_:float | None = None
    upper_:float | None = None

    def save(self,file_path:str) -> None:
        with open(file_path,'w') as file:
            json.dump(asdict(self),file,indent=2)

    def load(self,file_path:str) -> None:
        with open(file_path,'r') as file:
            data = json.load(file)
        self.iqr_boundary = data.get('iqr_boundary')
        self.lower_ = data.get('lower_')
        self.upper_ = data.get('upper_')