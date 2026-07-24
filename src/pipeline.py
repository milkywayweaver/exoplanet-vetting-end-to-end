from data import read_data,clean_data,split_data
from features import pl_features,pl_target
from model import tune_hyperparameter

from sklearn.svm import SVC

file_path = '../data/raw/TOI_2026.07.23_10.15.02.csv'

SEED = 42

# DATA ========================================================
raw = read_data(file_path=file_path)
data = clean_data(raw)
X_train,X_val,y_train,y_val = split_data(data,seed=SEED)

# PREPROCESSING
y_train, y_val = y_train.to_numpy(), y_val.to_numpy()
y_train = pl_target.fit_transform(y_train.reshape(-1,1)).flatten()
y_val = pl_target.transform(y_val.reshape(-1,1)).flatten()

# HYPERPARAMETER TUNING
param_grid = {
        'C': ['float',1e-2,1e1],
        'kernel':['cat',['linear','poly','rbf'],None],
        'degree':['int',2,4],
        'gamma':['cat',['scale'],None]
    }
best_param = tune_hyperparameter(SVC,param_grid,pl_features,X_train,y_train)