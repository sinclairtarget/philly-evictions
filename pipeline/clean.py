import pandas as pd
import numpy as np
from sklearn import preprocessing


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

    return df

####### FUNCTIONS TO RUN TO FIT ON TRAIN DATA ONLY ######

def get_feature_generators(train_df):
    feature_generator_dict = {}

    feature_generator_dict['scalers'] = create_scaler(train_df,['median_household_income'])
    feature_generator_dict['binaries'] = get_medians(train_df,['median_gross_rent'])

    return feature_generator_dict


####### FUNCTIONS TO RUN ON BOTH TRAIN AND TEST SEPARATELY ######

def clean_and_create_features(train_df, test_df, feature_generator_dict=None):

    #Impute missing values
    test_df = simple_imputation(test_df, ['black_alone_owner_occupied','for_rent_units',
        'median_gross_rent', 'median_household_income', 'num_af_am_alone', 'num_hisp',
        'num_unemployed', 'num_with_ged', 'num_with_high_school_degree',
        'occupied_units', 'renter_occupied_household_size', 'units','vacant_units'])

    train_df = simple_imputation(test_df, ['black_alone_owner_occupied','for_rent_units',
        'median_gross_rent', 'median_household_income', 'num_af_am_alone', 'num_hisp',
        'num_unemployed', 'num_with_ged', 'num_with_high_school_degree',
         'occupied_units', 'renter_occupied_household_size', 'units','vacant_units'])

    if feature_generator_dict:
        scalers = feature_generator_dict['scalers']
        binaries = feature_generator_dict['binaries']

        train_df, test_df = scale_data(train_df, test_df, scalers)
        train_df, test_df = binarize_data(train_df, test_df, binaries)

    train_df = drop_unwanted_columns(train_df, ['GEOID', 'year_evictions', 'year_features','median_household_income', 'median_gross_rent','eviction-filings'])
    test_df = drop_unwanted_columns(test_df, ['GEOID', 'year_evictions', 'year_features', 'median_household_income', 'median_gross_rent','eviction-filings'])

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

def simple_imputation(df, cols, method='median'):
    '''
    Takes in a dataframe, columns to impute from, and a method (which can be mean or median)
    '''
    for col in cols:
        if method == 'median':
            df[col].fillna(df[col].median(), inplace=True)

        elif method == 'mean':
            df[col].fillna(df[col].mean(), inplace=True)

    return df


def scale_data(train_df, test_df, scaler_dict):
    '''
    Scale data on training and apply to testing set leveraging scikitlearn function
    Inputs: training df, testing df, colum
    '''
    for col, scaler in scaler_dict.items():
        
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

def get_medians(train_df, cols):
    '''
    Create dict of cols and median vals in training data to apply on train + test in
    creating binary columns
    '''
    median_dict = {}

    for col in cols:
        median_dict[col] = train_df[col].median()

    return median_dict

def binarize_data(train_df, test_df, median_dict):
    '''
    Takes median dictionaries
    '''
    for col, median in median_dict.items():
        train_df[col+'_binary'] = np.where(train_df[col] >= median, 1, 0)
        test_df[col+'_binary'] = np.where(test_df[col] >= median, 1, 0)

    return train_df, test_df

def drop_unwanted_columns(df, cols_to_drop):
    '''
    Drops columns that will not be used in feature generation
    '''
    df = df.drop(cols_to_drop, axis=1)
    return df



