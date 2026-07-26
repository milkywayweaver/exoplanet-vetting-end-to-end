import optuna
from sklearn.base import BaseEstimator,clone
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import KernelPCA
import numpy as np
import mlflow

def tune_hyperparameter(model:BaseEstimator,param_grid:dict,preprocessing_pipeline:Pipeline,X:np.ndarray,y:np.ndarray,n_trials:int=50,scoring='accuracy',cpu:int=4) -> dict:
    '''
    Tune hyperparameter with Optuna.

    Args:
        model (BaseEstimator): Scikit-Learn classifier estimator to use for the model.
        param_grid (dict): Dictionary to construct Optuna trials. See example below.
            Structure:
                Use parameter name as key and a list for the value.
                The value list has three elements, with the first one being a string of the trial type.
                Supported trials are int, float, and categorical.
                For int and float, the second and third elements are mininum and maximum value respectively.
                For categorical, the second value is a list of all possible category and the third element being None.
                    - int: ['int', min_value, max_value]
                    - float: ['float', min_value, max_value]
                    - categorical: ['cat', [cat_1, cat_2, ..., cat_n], None]
            Example:
                PARAM_GRID = {
                        'C': ['float',1e-2,1e1],
                        'kernel':['cat',['linear','poly','rbf'],None],
                        'degree':['int',2,4],
                        'gamma':['cat',['scale'],None]
                    }
        preprocessing_pipeline (Pipeline): Scikit-Learn Pipeline object that is used for preprocessing the data.
        X (np.ndarray): Array of training data.
        y (np.ndarray): Array of target.
        n_trials (int, default=50): Number of trials run by Optuna.
        scoring (str: default="accuracy"): Scoring metric to evaluate hyperparameter combinations.
        cpu (int, default=4): Number of CPU to be used.
    '''
    def objective(trial):
        grid = {}
        for key,value in param_grid.items():
            match value[0]:
                case 'float':
                    grid[key] = trial.suggest_float(key,value[1],value[2])
                case 'int':
                    grid[key] = trial.suggest_int(key,value[1],value[2])
                case 'cat':
                    grid[key] = trial.suggest_categorical(key,value[1])

        pl = clone(preprocessing_pipeline)
        pl.steps.append(('model',model()))
        pl.set_params(**grid)

        with mlflow.start_run(nested=True):
            scores = cross_val_score(pl,X,y,cv=5,n_jobs=cpu,scoring=scoring)

            mlflow.log_params(grid)
            mlflow.log_metrics({
                'cv_recall_mean':scores.mean(),
                'cv_recall_std':scores.std()
            })
        return scores.mean()

    study = optuna.create_study(direction='maximize')
    study.optimize(objective,n_trials=n_trials)
        
    return study.best_params

if __name__ == '__main__':
    from sklearn.svm import SVC
    from sklearn.datasets import load_breast_cancer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    loader =  load_breast_cancer()
    X = loader.data
    y = loader.target

    pl = Pipeline([
        ('scaler',StandardScaler())
    ])

    PARAM_GRID = {
        'C': ['float',1e-2,1e1],
        'kernel':['cat',['linear','poly','rbf'],None],
        'degree':['int',2,4],
        'gamma':['cat',['scale'],None]
    }
    result = tune_hyperparameter(SVC,PARAM_GRID,pl,X,y,cpu=4)
    print(result)
