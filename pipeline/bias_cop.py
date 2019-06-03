import numpy as np
from aequitas.preprocessing import preprocess_input_df
from aequitas.group import Group
from aequitas.plotting import Plot
import ipdb

class BiasCop:
    """
    Wraps Aequitas. Returns metrics measuring bias and fairness of our models.

    Generates "fairness" groups based on the majority demographic in a
    neighborhood.
    """
    DEFAULT_CONFIG = {
        'label_col': 'label',
        'score_col': 'score',
        'population_col': 'total_population',
        'demographic_features': ['num_af_am_alone', 'num_hisp']
    }

    def __init__(self, results_df, **kwargs):
        self.config = BiasCop.DEFAULT_CONFIG.copy()
        self.config.update(kwargs)
        self.results_df = self._preprocess(results_df)
        self.xtab = None


    def xtabs(self):
        """
        Returns a dataframe with lots of different metrics for each feature
        in the original input dataframe.
        """
        # Cache it
        if self.xtab is not None:
            return self.xtab

        self.xtab, _ = Group().get_crosstabs(self.results_df)
        return self.xtab


    def plot_group_metric(self, metric):
        """
        Returns a plot. You may have to call plt.show() using matplotlib in
        order to see anything.
        """
        xtab = self.xtabs()
        plot = Plot().plot_group_metric(xtab, metric)
        return plot


    def _preprocess(self, df):
        df = self._create_groups(df)

        # Temp hack for now
        score_col = self.config['score_col']
        df[score_col] = 1

        # Aequitas wants the label column to be called by this name
        label_col = self.config['label_col']
        df['label_value'] = df[label_col]
        df = df.drop(columns=[label_col])

        # Make sure group col is a string
        df.majority_demo = df.majority_demo.astype(str)

        # Filter to only what Aequitas needs
        columns = ['label_value', score_col, 'majority_demo']
        df, _ = preprocess_input_df(df[columns])

        return df


    def _create_groups(self, df):
        groups = df.apply(lambda row: self._majority(row), axis=1)
        return df.assign(majority_demo=groups.values)


    def _majority(self, df_row):
        pop_col = self.config['population_col']

        for demo in self.config['demographic_features']:
            # If we don't have the data, we might miss some majority demos :(
            demo_count = self._filter_nan(df_row[demo])
            total_pop = self._filter_nan(df_row[pop_col], fallback=demo_count)

            if (total_pop > 0 and (demo_count / total_pop) > 0.5):
                return demo

        return 'other'


    def _filter_nan(self, val, fallback=0):
        if val == np.nan:
            return fallback
        elif np.isinf(val):
            return fallback
        else:
            return val or fallback
