import pandas as pd
import numpy as np
from sklearn import preprocessing

# Master function to clean a split
def clean_split(split):
    train_df, test_df = split
    train_df = clean_overall_data(train_df)
    test_df = clean_overall_data(test_df)

    features_generator = get_feature_generators(train_df)
    train_df, test_df = \
        clean_and_create_features(train_df, test_df, features_generator)

    return train_df, test_df


####### FUNCTIONS TO RUN PRE-TRAIN_TEST SPLIT ######

def clean_overall_data(complete_df):
    '''
    Execute cleaning steps prior to splitting into test and train
    '''
    df = clean_period_as_missing(complete_df)
    df = convert_to_numeric(df, ['renter_occupied_household_size','median_gross_rent',
        'median_household_income'])
    df = clean_missing_vals(df)
    df = impute_as_zero(df, ['violations_count','crime_count'])
    df = get_change_in_feature(df, 'evictions', ['evictions_t-1',
        'evictions_t-2','evictions_t-5'])
    df = get_pct_feature(df, 'crime_count', 'total_population')
    df = get_pct_feature(df, 'violations_count', 'total_population')
    df = get_pct_feature(df, 'total_renter_households', 'total_households')
    df = get_pct_feature(df, 'vacant_units', 'units')
    df = get_pct_feature(df, 'for_rent_units', 'units')
    df = get_pct_feature(df, 'num_af_am_alone', 'total_population')
    df = get_pct_feature(df, 'num_hisp', 'total_population')
    df = get_pct_feature(df, 'black_alone_owner_occupied', 'units')
    df = get_pct_feature(df, 'num_with_high_school_degree', 'total_population')
    df = get_pct_feature(df, 'num_with_ged', 'total_population')
    df = get_pct_feature(df, 'num_unemployed', 'total_population')
    df['majority_af_am'] = np.where(df['num_af_am_alone_percent'] > .5, 1, 0)
    df['majority_hisp'] = np.where(df['num_hisp_percent'] > .5, 1, 0)
    df['evictions_change_1_binary'] = np.where(df['num_hisp_percent'] > 0, 1, 0)
    df['evictions_change_2_binary'] = np.where(df['num_hisp_percent'] > 0, 1, 0)
    df['evictions_change_5_binary'] = np.where(df['num_hisp_percent'] > 0, 1, 0)

    return df

####### FUNCTIONS TO RUN TO FIT ON TRAIN DATA ONLY ######

def get_feature_generators(train_df):
    feature_generator_dict = {}

    feature_generator_dict['scalers'] = create_scaler(train_df,['evictions_t-1', 'evictions_t-2', 'evictions_t-5',
        'crime_count', 'violations_count', 'total_population',
        'total_households', 'total_renter_households',
        'renter_occupied_household_size', 'median_gross_rent',
        'median_household_income', 'units', 'occupied_units', 'vacant_units',
        'for_rent_units', 'num_af_am_alone', 'num_hisp',
        'black_alone_owner_occupied', 'num_with_high_school_degree',
        'num_with_ged', 'num_unemployed'])
    feature_generator_dict['binaries'] = get_binary_cutoffs(train_df,
        {'crime_count_percent': .9, 'violations_count_percent': .9,
        'vacant_units_percent': .5, 'total_renter_households_percent': .5,
        'num_unemployed_percent': .5})

    return feature_generator_dict


####### FUNCTIONS TO RUN ON BOTH TRAIN AND TEST SEPARATELY ######

def clean_and_create_features(train_df, test_df, feature_generator_dict=None):

    #Impute missing values

    train_df = train_df.fillna(train_df.median())
    train_df = train_df.dropna(axis=1, how='all')
    test_df = test_df.fillna(test_df.median())
    test_df = test_df.dropna(axis=1, how='all')

    test_df = check_col_match(train_df, test_df)

    if feature_generator_dict:
        scalers = feature_generator_dict['scalers']
        binaries = feature_generator_dict['binaries']

        train_df, test_df = scale_data(train_df, test_df, scalers)
        train_df, test_df = binarize_data(train_df, test_df, binaries)

    return train_df, test_df


###### HELPER FUNCTIONS ######

def clean_period_as_missing(df):
    '''
    Reformats missing values represented as a period to be a numpy NaN value
    '''
    df = df.replace('^\.$', np.nan, regex=True)
    return df

def clean_missing_vals(df):
    '''
    Reformats known missing number values as nans
    '''
    df = df.replace(-666666666, np.nan)
    return df

def convert_to_numeric(df, cols):
    '''
    Converts columns which contain numbers in string format to integers
    '''
    df[cols] = df[cols].apply(pd.to_numeric)
    return df

def impute_as_zero(df, cols):
    '''
    Imputs missing values as 0 (for where no data means that this field was
    not present, e.g. no crimes occurred)
    '''
    for col in cols:
        df[col].fillna(0.0, inplace=True)

    return df

def scale_data(train_df, test_df, scaler_dict):
    '''
    Scale data on training and apply to testing set leveraging scikitlearn function
    Inputs: training df, testing df, colum
    '''
    for col, scaler in scaler_dict.items():

        if col not in train_df.columns:
            continue

        train_df[col+'_scaled'] = scaler.transform(train_df[[col]])
        test_df[col+'_scaled'] = scaler.transform(test_df[[col]])

    return train_df, test_df

def create_scaler(train_df, cols):
    '''
    Creates scalers for relevant columns in a dataframe
    '''

    scaler_dict = {}

    for col in cols:
        scaler = preprocessing.StandardScaler()
        scaler = scaler.fit(train_df[[col]])
        scaler_dict[col] = scaler

    return scaler_dict

def get_binary_cutoffs(train_df, col_quantile_dict):
    '''
    Create dict of cols and median vals in training data to apply on train + test in
    creating binary columns
    '''
    return_dict = {}

    for col, q in col_quantile_dict.items():
        return_dict[col] = train_df[col].quantile(q=q)

    return return_dict

def binarize_data(train_df, test_df, quantile_dict):
    '''
    Takes median dictionaries
    '''
    for col, quantile in quantile_dict.items():

        if col not in train_df.columns:
            continue
            
        train_df[col+'_binary'] = np.where(train_df[col] >= quantile, 1, 0)
        test_df[col+'_binary'] = np.where(test_df[col] >= quantile, 1, 0)

    return train_df, test_df

def drop_unwanted_columns(df, cols_to_drop):
    '''
    Drops columns that will not be used in feature generation
    '''
    df = df.drop(cols_to_drop, axis=1)
    return df

def get_change_in_feature(df, col, historical_cols):
    '''
    Creates a new feature of % change from t - time horizon year
    '''
    for historical_col in historical_cols:
        time_horizon = historical_col[-1]
        df[col+'_change'+'_'+time_horizon] = (df[col] - df[historical_col])/df[historical_col]
        
        df[col+'_change'+'_'+time_horizon] = np.where((df[col] == 0.0) & (df[historical_col] == 0.0), 
            0.0, df[col+'_change'+'_'+time_horizon])

        df[col+'_change'+'_'+time_horizon] = np.where(df[historical_col] == 0.0, 
            1.0 * df[historical_col], df[col+'_change'+'_'+time_horizon])
    
    return df

def get_pct_feature(df, numerator_col, denom_col):
    '''
    Create a percentage column
    '''
    df[numerator_col+'_percent'] = df[numerator_col]/df[denom_col]
    return df

def check_col_match(train_df, test_df):
    '''
    Remove cols from test that do not appear in training
    '''
    extra_cols = []

    for column in test_df.columns:
        if column not in train_df.columns:
            extra_cols.append(column)

    test_df = test_df.drop(extra_cols,axis=1)

    return test_df




