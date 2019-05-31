import pandas as pd
from functools import reduce

## Import features data
crime_df = pd.read_csv('data/crime_data.csv', index_col='Unnamed: 0')
violations_df = pd.read_csv('data/violations.csv', index_col='Unnamed: 0')
acs_2009_2012_df = pd.read_csv('data/acs_2009_2012.csv')
acs_2013_2016_df = pd.read_csv('data/acs_2013_2016.csv')

# Merge features data
acs_df = acs_2009_2012_df.append(acs_2013_2016_df, sort=False)
features_dfs = [crime_df, violations_df, acs_df]
features_merged = reduce(lambda left, right: pd.merge(
    left, right, on=['GEOID', 'year'], how='outer'), features_dfs)
features_merged = features_merged[features_merged['year'] >= 2009]

# Create lag variable to merge features and evictions data 
features_merged['lag'] = features_merged['year'] + 1

# Import evictions data
evictions_df = pd.read_csv('data/block-groups_pa.csv')
evictions_df = evictions_df[evictions_df['parent-location'] == 'Philadelphia County, Pennsylvania']
evictions_df = evictions_df[evictions_df['year'] >= 2010]
evictions_df = evictions_df[['GEOID', 'year', 'name', 'parent-location', 
'eviction-filings', 'evictions', 'low-flag', 'imputed', 'subbed']]

# Merge evictions data with features data 
final_merged_df = pd.merge(evictions_df, features_merged, 
                           left_on=['GEOID', 'year'], right_on=['GEOID', 'lag'], how='left')
final_merged_df.drop(columns=['name', 'parent-location', 'lag'], inplace=True)
final_merged_df.rename(columns={'year_x': 'year_evictions', 'year_y': 'year_features'}, inplace=True)

# Export to csv 
final_merged_df.to_csv('data/final_merged_df.csv', index=False)