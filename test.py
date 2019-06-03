import pandas as pd
import numpy as np
import pipeline

df = pd.read_csv('data/final_merged_df.csv')

splits = pipeline.split_by_year(df, colname='year_evictions')
cleaned_splits = [pipeline.clean_split(split) for split in splits]
labeled_splits = [pipeline.label(split, lower_bound=10, drop_column=True)
                  for split in cleaned_splits]

#thresholds = [10]
#
#models = pipeline.clfs
#grid = pipeline.clf_small_grid
#
#results_df = pd.DataFrame(columns=[
#    'classifier',
#    'parameters',
#    'threshold',
#    'split',
#] + pipeline.evaluate.ClassifierEvaluator.metric_names())
#
#for train_df, test_df in labeled_splits:
#    results = pipeline.run_clf_loop(
#        test_df, train_df, models, grid, 'label', thresholds
#    )
#    results_df.append(results, ignore_index=True)
