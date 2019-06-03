import numpy as np
import pandas as pd

def label(split, lower_bound, drop_column=False):
    train_df, test_df = split
    train_df = train_df.copy() # Err, think about why this is needed later
    test_df = test_df.copy()

    train_df['label'] = \
            np.where(train_df['evictions'] > lower_bound, 1, 0)
    test_df['label'] = \
            np.where(test_df['evictions'] > lower_bound, 1, 0)

    if drop_column:
        train_df = train_df.drop(columns=['evictions'])
        test_df = test_df.drop(columns=['evictions'])

    return train_df, test_df
