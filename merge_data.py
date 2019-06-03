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
evictions_df = evictions_df[['GEOID', 'year', 'name', 'parent-location', 
                             'evictions', 'low-flag', 'imputed', 'subbed']]

# Create evictions_t-1, t-2, t-5 features
evictions_wide = evictions_df.pivot(index='GEOID', columns='year', values='evictions')
evictions_lag = pd.merge(evictions_df, evictions_wide, left_on='GEOID', right_index=True)
evictions_lag.head()
for year in range(2010, 2017): 
    evictions_t_1 = year - 1 
    evictions_t_2 = year - 2
    evictions_t_5 = year - 5
    evictions_lag.loc[evictions_lag['year'] == year, 'evictions_t-1'] = evictions_lag[evictions_t_1]
    evictions_lag.loc[evictions_lag['year'] == year, 'evictions_t-2'] = evictions_lag[evictions_t_2]
    evictions_lag.loc[evictions_lag['year'] == year, 'evictions_t-5'] = evictions_lag[evictions_t_5]
evictions_lag = evictions_lag[['GEOID', 'year', 'evictions_t-1', 'evictions_t-2', 'evictions_t-5']]    
evictions_merged = pd.merge(evictions_df, evictions_lag, on=['GEOID', 'year']) 

# Merge evictions data with features data 
final_merged_df = pd.merge(evictions_merged, features_merged, 
                           left_on=['GEOID', 'year'], right_on=['GEOID', 'lag'], how='left')
final_merged_df.drop(columns=['name', 'parent-location', 'lag', 'year_y'], inplace=True)
final_merged_df.rename(columns={'year_x': 'year_evictions'}, inplace=True)
final_merged_df = final_merged_df[final_merged_df['year_evictions'] >= 2010]

# Export to csv 
final_merged_df.to_csv('data/final_merged_df.csv', index=False)