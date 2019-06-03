import numpy as np
import pandas as pd

def check_any_nan_or_inf(df, name='df'):
    """
    Checks a dataframe to see if it contains NaN or infinity values.
    """
    for colname in df.columns:
        if np.isnan(df[colname]).any():
            raise Exception(f"Found a NaN in column {colname} in {name}.")
        elif not np.isfinite(df[colname].values).all():
            raise Exception(f"Found an Inf in column {colname} in {name}.")
