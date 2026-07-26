import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import great_expectations as gx
import great_expectations.expectations as gxe

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

def validate_data(data:pd.DataFrame):
    '''
    Validates raw data before data cleaning is performed.

    Args:
        data (pd.DataFrame): The raw data to validate.
            Validations including column existance and value checks.
    Return:
        None
    '''
    print(f'Starting data validation...')
    # Input checks
    raw_cols = ['rowid', 'toi', 'toipfx', 'tid', 'ctoi_alias', 'pl_pnum', 'tfopwg_disp',
       'rastr', 'ra', 'decstr', 'dec', 'st_pmra', 'st_pmdec', 'pl_tranmid',
       'pl_orbper', 'pl_trandurh', 'pl_trandep', 'pl_rade', 'pl_insol',
       'pl_eqt', 'st_tmag', 'st_dist', 'st_teff', 'st_logg', 'st_rad',
       'toi_created', 'rowupdate']
    expectations = [gxe.ExpectColumnToExist(column=col) for col in raw_cols]

    # Value checks
    values_expectation = {
        'ra':{
            'expectation_type':'values_between',
            'min_value':0,
            'max_value':360,
            'mostly':1
        },
        'dec':{
            'expectation_type':'values_between',
            'min_value':-90,
            'max_value':90,
            'mostly':1
        },
        'pl_tranmid':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_orbper':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_trandurh':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_trandep':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_rade':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_insol':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'pl_eqt':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'st_tmag':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'st_dist':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'st_teff':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'st_logg':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'st_rad':{
            'expectation_type':'min_values',
            'min_value':0,
            'max_value':None
        },
        'tfopwg_disp':{
            'expectation_ttype':'values_in',
            'list':['APC','FA','FP','KP','PC','CP'],
            'mostly':1
        },
        'tfopwg_disp':{
            'expectation_type':'non_null',
            'mostly':0.95
        }
    }
    for key,value in values_expectation.items():
        match value['expectation_type']:
            case 'values_between':
                expectation = gxe.ExpectColumnValuesToBeBetween(column=key,min_value=value['min_value'],max_value=value['max_value'],mostly=value['mostly'])
            case 'min_values':
                expectation = gxe.ExpectColumnMinToBeBetween(column=key,min_value=value['min_value'],max_value=value['max_value'])
            case 'values_in':
                expectation = gxe.ExpectColumnnValuesToBeInSet(column=key,value_set=value['list'],mostly=value['mostly'])
            case 'non_null':
                expectation = gxe.ExpectColumnValuesToNotBeNull(column=key,mostly=value['mostly'])
        expectations.append(expectation)

    # Adds the data to the context 
    context = gx.get_context()
    source = context.data_sources.add_pandas('pandas')
    asset = source.add_dataframe_asset(name='TESS TOI')
    batch_definition = asset.add_batch_definition_whole_dataframe('whole')

    # Adds the expectations to the context
    suite = gx.ExpectationSuite(name='TESS Data Expectations',expectations=expectations)
    suite = context.suites.add(suite)

    # Adds validation schemes to the context
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name='TESS TOI Table Validation',
            data=batch_definition,
            suite=suite
        )
    )

    results = validation_definition.run(batch_parameters={'dataframe':data})
    print(f'Data validation success: {results.success}.')
    print(f'Statistics: {results.success}')

    if not results.success:
        print('EXPECTATIONS ARE NOT MET')
        i = 0
        for result in results.results:
            if not result.success:
                failed_expectation = result.expectation_config
                print(f'{i} - Expectation {failed_expectation.type} on column {failed_expectation.kwargs['column']} is not met.')
                i += 1

if __name__ == '__main__':
    file_path = '../data/raw/TOI_2026.07.23_10.15.02.csv'
    raw = read_data(file_path=file_path)
    validate_data(raw)
    data = clean_data(raw)
   