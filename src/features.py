from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.decomposition import PCA
from modules.aslt import ASLT

pl_features = Pipeline([
    ('imputer',KNNImputer(n_neighbors=10)),
    ('autolog',ASLT(beta=20)),
    ('scaler',StandardScaler()),
    ('pca',PCA()),
])
pl_target = Pipeline([
    ('encoder',OrdinalEncoder(categories=[['F','C','PC']]))
])