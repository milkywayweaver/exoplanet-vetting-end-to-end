from sklearn.base import BaseEstimator,TransformerMixin
import numpy as np

class OutlierRemoval(BaseEstimator,TransformerMixin):
    '''
    Outlier removal module.
    '''
    def __init__(self,iqr_boundary:float=1.5,print_detail:bool=False):
        '''
        Initializes outlier removal module using IQR method.

        Args:
            iqr_boundary (float): IQR boundary value to use
            print_detail (bool): Whether to print count of removed rows or not
        Returns:
            None
        '''
        self.iqr_boundary = iqr_boundary
        self.print_detail = print_detail

    def fit(self,X_and_y):
        X,y = X_and_y
        X = np.asarray(X,dtype=np.float32)
        median = np.nanmedian(X,axis=0)
        q3 = np.nanpercentile(X,75,axis=0)
        q1 = np.nanpercentile(X,25,axis=0)
        iqr = q3 - q1

        self.lower_ = median - self.iqr_boundary*iqr
        self.upper_ = median + self.iqr_boundary*iqr
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