from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from modules.aslt import ASLT

pl_features = Pipeline([
    ('imputer',KNNImputer(n_neighbors=10)),
    ('autolog',ASLT(beta=20)),
    ('scaler',StandardScaler())
])
pl_target = Pipeline([
    ('encoder',OrdinalEncoder(categories=[['F','C','PC']]))
])