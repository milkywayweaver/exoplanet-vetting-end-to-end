from data import read_data,clean_data,split_data,validate_data
from features import pl_features,pl_target
from model import tune_hyperparameter
from evaluate import evaluate_metrics,plot_confmat

import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.base import clone
from sklearn.model_selection import cross_val_score
import mlflow

file_path = '../data/raw/TOI_2026.07.23_10.15.02.csv'

SEED = 42
RUN_NAME = 'SVC'
N_TRIALS = 20
CV_SCORING = 'precision'

# DATA ========================================================
print('Reading data...')
raw = read_data(file_path=file_path)
validate_data(raw)
data = clean_data(raw)
X_train,X_val,y_train,y_val = split_data(data,seed=SEED)

# PREPROCESSING
y_train, y_val = y_train.to_numpy(), y_val.to_numpy()
y_train = pl_target.fit_transform(y_train.reshape(-1,1)).flatten()
y_val = pl_target.transform(y_val.reshape(-1,1)).flatten()
cats = pl_target.named_steps['encoder'].categories[0]

# HYPERPARAMETER TUNING
print('Starting hyperparameter tuning...')
param_grid = {
    'pca__kernel':['linear','poly','rbf'],
    'model__C': ['float',1e-2,1e1],
    'model__kernel':['cat',['linear','poly','rbf'],None],
    'model__degree':['int',2,4],
    'model__gamma':['cat',['scale'],None]
    }
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment('TESS Planetary Candidate Experiments')
with mlflow.start_run(run_name=f'{RUN_NAME}_EXPERIMENT'):
    best_param = tune_hyperparameter(SVC,param_grid,pl_features,X_train,y_train,n_trials=N_TRIALS,scoring=CV_SCORING)

# MODELLING
print('Modelling with the best hyperparameter...')
mlflow.set_experiment('TESS Planetary Candidate Models')
pl_complete = clone(pl_features)
pl_complete.steps.append(('model',SVC()))
pl_complete.set_params(**best_param)
pl_complete.fit(X_train,y_train)
preds_val = pl_complete.predict(X_val)

with mlflow.start_run(run_name=f'{RUN_NAME}_MODEL'):
    scores = cross_val_score(pl_complete,X_train,y_train,cv=5,n_jobs=4,scoring=CV_SCORING)
    metrics_val = evaluate_metrics(y_val,preds_val,binary=True)
    fig = plt.figure(figsize=(6,5))
    plot_confmat(y_val,preds_val,cats[:2])
    plt.close()

    mlflow.log_params(best_param)
    mlflow.log_metrics({
        'cv_recall_mean':scores.mean(),
        'cv_recall_std':scores.std()
    })
    mlflow.log_metrics(metrics_val)
    mlflow.sklearn.log_model(
        pl_complete,
        name='model',
        serialization_format='skops',
        skops_trusted_types=['modules.aslt.ASLT']
        )
    mlflow.log_figure(fig,'confmat.png')