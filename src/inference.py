import pandas as pd
from mlflow.pyfunc import PyFuncModel
from data import validate_data,clean_data

def predict_full(data:dict,model:PyFuncModel) -> list:
    '''
    Takes dictionary input with TOI table columns as keys.
    Must include all TOI columns INCLUDING "tfopwg_disp" --> "PC" for unknown disposition.

    Args:
        data (dict): A dictionary containing TOI table data with the keys as columns.
        model (PyFuncModel): The model in PyFunc format.
    Returns:
        List of 0 (False detection) or 1 (Confirmed planet) predictions.
    '''
    raw = pd.DataFrame(data)
    validate_data(raw)
    cleaned_df = clean_data(raw)

    X = cleaned_df.drop('disp',axis=1)

    preds = model.predict(X)
    return preds

def predict(data:dict,model:PyFuncModel) -> list:
    '''
    Takes dictionary input with TOI table columns as keys.
    
    Args:
        data (dict): A dictionary containing TOI table data with the keys as columns.
            Required keys are: 
                    - "ra"
                    - "dec" 
                    - "st_pmra"
                    - "st_pmdec"
                    - "pl_tranmid"
                    - "pl_orbper"
                    - "pl_trandurh"
                    - "pl_trandep"
                    - "pl_rade"
                    - "pl_insol"
                    - "pl_eqt"
                    - "st_tmag"
                    - "st_dist"
                    - "st_teff"
                    - "st_logg"
                    - "st_rad"
        model (PyFuncModel): The model in PyFunc format.
    Returns:
        List of 0 (False detection) or 1 (Confirmed planet) predictions.
    '''
    missing_cols = ['rowid','toi','toipfx','tid','ctoi_alias','pl_pnum','rastr','decstr','toi_created','rowupdate','tfopwg_disp']
    data_keys = list(data.keys())
    for col in missing_cols:
        if col not in data_keys:
            data[col] = ''
    raw = pd.DataFrame([data])
    validate_data(raw)
    cleaned_df = clean_data(raw)

    X = cleaned_df.drop('disp',axis=1)

    preds = model.predict(X).astype(int).tolist()
    return preds  

if __name__ == '__main__':
    data = {'ra':34.12,
            'dec':88.3,
            'st_pmra':-5.964,
            'st_pmdec':-0.076,
            'pl_tranmid':2.459230e6,
            'pl_orbper':2.171348,
            'pl_trandurh':2.017220,
            'pl_trandep':656.886099,
            'pl_rade':5.818163,
            'pl_insol':22601.948581,
            'pl_eqt':3127.204052,
            'st_tmag':9.604000,
            'st_dist':485.735,
            'st_teff':10249.0,
            'st_logg':4.19,
            'st_rad':2.169860}

    preds = predict(data)
    print(preds)
