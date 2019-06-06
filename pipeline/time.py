import pandas as pd

def split_by_year(df, colname='year', drop_col=False):
    """
    Returns a list of two-tuples where the first element in the tuple is a
    training set dataframe and the second element is the corresponding test set
    dataframe. There is a test set for each year except the first. The training
    set is only ever the previous year.

    For example, given a dataframe with data for 2012, 2013, 2014, and 2015
    this function returns dataframes for the years:

    [(2012, 2013), (2013, 2014), (2014, 2015)]
    """
    min_year = df[colname].min()
    max_year = df[colname].max()
    years = range(min_year, max_year + 1)
    year_tuples = zip(years[:-1], years[1:])
    return [_df_tuple(df, colname, drop_col, year_tuple)
            for year_tuple in year_tuples]


def split_boundaries(splits, colname='year'):
    """
    Returns a dataframe that clearly shows the start and end boundaries of all
    the training and test sets in the given list of splits.
    """
    df = pd.DataFrame(columns=[
        'train_start', 'train_end', 'test_start', 'test_end'
    ])

    for train_df, test_df in splits:
        train_min = train_df[colname].min()
        train_max = train_df[colname].max()
        test_min = test_df[colname].min()
        test_max = test_df[colname].max()
        df = df.append({
            'train_start': train_min,
            'train_end': train_max,
            'test_start': test_min,
            'test_end': test_max
        }, ignore_index=True)

    return df


def _df_tuple(df, colname, drop_col, year_tuple):
    train_year, test_year = year_tuple
    train_df = df[df[colname] == train_year]
    test_df = df[df[colname] == test_year]

    if drop_col:
        train_df = train_df.drop(columns=[colname])
        test_df = test_df.drop(columns=[colname])

    return train_df, test_df
