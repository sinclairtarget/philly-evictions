import pandas as pd
import numpy as np
from sklearn import preprocessing


####### FUNCTIONS TO RUN PRE-TRAIN_TEST SPLIT ######

def clean_overall_data(complete_df):
    '''
    Execute cleaning steps prior to splitting into test and train
    '''
    df = clean_missing_vals(complete_df)
    df = clean_period_as_missing(df)
    df = convert_to_numeric(df, ['renter_occupied_household_size','median_gross_rent',
        'median_household_income'])
    df = impute_as_zero(df, ['violations_count','crime_count'])

    return df

####### FUNCTIONS TO RUN TO FIT ON TRAIN DATA ONLY ######

def create_scaler(train_df, cols):
    '''
    Creates scalers for relevant columns in a dataframe
    '''

    scaler_dict = {}

    for col in cols:
        scaler = preprocessing.StandardScaler()
        scaler.fit(train_df[[col]])
        scaler_dict[col] = scaler

    return scaler_dict

####### FUNCTIONS TO RUN ON BOTH TRAIN AND TEST SEPARATELY ######

def clean_and_create_features(train_df, test_df, scaler=None):

    #Impute missing values
    test_df = simple_imputation(test_df, ['black_alone_owner_occupied','for_rent',
        'median_gross_rent', 'median_household_income', 'num_af_am_alone', 'num_hisp',
        'num_unemployed', 'num_with_ged', 'num_with_high_school_degree',
        'occupied', 'renter_occupied_household_size', 'units'])

    train_df = simple_imputation(test_df, ['black_alone_owner_occupied','for_rent',
        'median_gross_rent', 'median_household_income', 'num_af_am_alone', 'num_hisp',
        'num_unemployed', 'num_with_ged', 'num_with_high_school_degree',
         'occupied', 'renter_occupied_household_size', 'units'])

    if scaler:
        train_df, test_df = scale_data(train_df, test_df, scaler)

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
        
        #Fit the columns
        train_df[col] = scaler.transform(train_df[[col]])
        test_df[col] = scaler.transform(test_df[[col]])

        #Clamp the testing data
        test_df[col] = np.where(test_df[col] < 0, 0, test_df[col])
        test_df[col] = np.where(test_df[col] > 1, 1, test_df[col])

    return train_df, test_df
