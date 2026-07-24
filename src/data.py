import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def read_data(file_path:str) -> pd.DataFrame:
    '''
    Reads a TESS CSV table downloaded with "Values only" option enabled.

    Args:
        file_path (str): The path to the TESS CSV table.
    Returns:
        pd.DataFrame table of raw TESS data. 
    '''
    if not file_path.endswith('.csv'):
        raise ValueError(f'Invalid file path! Please make sure the file is a CSV file!')
    data = pd.read_csv(file_path,skiprows=30)
    return data

def clean_data(data) -> pd.DataFrame:
    '''
    Clean raw TESS table read from read_data function.
    Data cleaning includes:
        1. Dropping identifier columns.
        2. Converting RA and dec into their trigonometry variant to ensure cyclic properties.
        3. Renaming and grouping disposition into false detection ("F"), confirmed planet ("C"), and planetary candidate ("PC").

    Args:
        data (pd.DataFrame): Pandas DataFrame of TESS table obtained from read_data function.
    Returns:
        pd.DataFrame table of cleaned TESS data.
    '''
    df = data.drop(['rowid','toi','toipfx','tid','ctoi_alias','pl_pnum','rastr','decstr','toi_created','rowupdate'],axis=1)

    # Since RA and declination are cyclic, convert them into their sin() and cos() values to ensure cyclic behaviour
    df.insert(0,'cos_dec',np.cos(np.radians(df['dec'])))
    df.insert(0,'sin_dec',np.sin(np.radians(df['dec'])))
    df.insert(0,'cos_ra',np.cos(np.radians(df['ra'])))
    df.insert(0,'sin_ra',np.sin(np.radians(df['ra'])))

    df = df.drop(['ra','dec'],axis=1)

    # Drop rows with missing disposition (target) value
    df['disp'] = df.pop('tfopwg_disp')
    df = df.dropna(subset=['disp'])

    # Group dispositions into three groups
    disp_map = {'APC':'PC',
                'FA':'F',
                'FP':'F',
                'KP':'C',
                'PC':'PC',
                'CP':'C'}
    df['disp'] = df['disp'].map(disp_map)
    return df

def split_data(data,seed=42):
    '''
    Splits the cleaned TESS table into training and validation set.
    Only processes rows with disposition group of "F" and "C".
    
    Args:
        data (pd.DataFrame): Cleaned TESS table.
        seed (int): Random seed for splitting reproducability.
    Returns:
        tuple of the resulting split:
            (X_train (pd.DataFrame), X_val (pd.DataFrame), y_train (pd.Series), y_val (pd.Series))
    '''
    df = data[data['disp'] != 'PC']
    X = df.drop('disp',axis=1)
    y = df['disp']

    X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.2,random_state=seed,stratify=y)
    return X_train,X_val,y_train,y_val