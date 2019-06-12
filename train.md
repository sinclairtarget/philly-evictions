# Philly Evictions Model Training
## Environment Setup
```python
import pandas as pd
import numpy as np
import pipeline

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pipeline.notebook.set_up()
```

## Load Data
Our evictions data has already been augmented with data from the ACS and from
Philadelphia's open data portal. We load in the final merged dataset.

```python
df = pd.read_csv('data/final_merged_df.csv')
df.head()
```

## Split Data By Year
We have data for 2009 to 2016. We want to split this data into training set /
test set pairs using a temporal cross-validation approach.

```python
split_output_filename = 'results/time_splits/time_split_ay.csv'
clf_output_filename = 'results/evaluation_results/clf-small-grid_ay.csv'
reg_output_filename = 'results/evaluation_results/reg-small-grid_ay.csv'
splits = pipeline.split_all_years(df, colname='year_evictions')

split_table = pipeline.split_boundaries(splits, colname='year_evictions')
split_table.to_csv(split_output_filename, index=False)
```

## Data Cleaning
We want to clean each of our training set / test set pairs. We use a function
called `clean_split()` that cleans both sets at once, making sure to clean the
test data using the same bins and categories applied to the training data.

```python
%psource pipeline.clean_split
```
```python
cleaned_splits = [pipeline.clean_split(split) for split in splits]
```

## Data Labeling
We plan to use both regression-based models and binary classifiers. For our
binary classifiers, we will need to label our data using a binary label.

Our binary label separates block groups into two classes: "high" and "low"
eviction rate block groups. The "high" eviction rate block groups are those
that we believe should be prioritized for intervention.

Any block group with more than 14 evictions is considered a "high" eviction
rate block group. Roughly 16% of Philadelphia block groups are "high" eviction
rate block groups. We have picked this lower boundary because we know that
Philadelphia can afford to target about 16% of block groups for intervention.

```python
labeled_splits = [pipeline.label(split, lower_bound=15, drop_column=True)
                  for split in cleaned_splits]
```

## Model Generation
### Binary Classifiers
```python
clfs = pipeline.clfs
clfs_grid = pipeline.clf_small_grid
```

Our binary classifiers are given by the following list:
```python
clfs
```

We plan to run a grid search using the following hyperparameters.
```python
clfs_grid
```

We also want to evaluate our models at the following thresholds:
```python
thresholds = [14, 21, 28]
```

We run our models for each of our splits.
```python
results_df = pd.DataFrame(columns=[
    'split',
    'classifier',
    'parameters',
    'threshold'
] + pipeline.evaluate.ClassifierEvaluator.metric_names())

for i, (train_df, test_df) in enumerate(labeled_splits, start=1):
    train_df = train_df.drop(columns=['GEOID', 'year_evictions'])
    test_df = test_df.drop(columns=['GEOID', 'year_evictions'])
    df = pipeline.run_clf_loop(
        test_df, train_df, clfs, clfs_grid, 'label', thresholds, debug=False
    )

    df = df.assign(split=i)
    results_df = results_df.append(df, ignore_index=True)

results_df.to_csv(clf_output_filename, index=False)
```

### Regression Models
```python
regs = pipeline.regs
regs_grid = pipeline.reg_small_grid
```

Our regression models are given by the following list:

```python
regs
```

We plan to run a grid search using the following hyperparameters:
```python
regs_grid
```

We run our models for each of our splits.
```python
results_df = pd.DataFrame(columns=[
    'split',
    'classifier',
    'parameters',
] + pipeline.evaluate.RegressionEvaluator.metric_names())

for i, (train_df, test_df) in enumerate(cleaned_splits, start=1):
    train_df = train_df.drop(columns=['GEOID', 'year_evictions'])
    test_df = test_df.drop(columns=['GEOID', 'year_evictions'])
    df = pipeline.run_reg_loop(
        test_df, train_df, regs, regs_grid, 'evictions'
    )

    df = df.assign(split=i)
    results_df = results_df.append(df, ignore_index=True)

results_df.to_csv(reg_output_filename, index=False)
```
