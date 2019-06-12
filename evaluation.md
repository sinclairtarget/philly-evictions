---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Model Evaluation
```python
# Imports + read in files
from pipeline import find_best_model
import pandas as pd
import matplotlib.pyplot as plt

reg_df = pd.read_csv('results/reg-small-grid_ay.csv')
clf_df = pd.read_csv('results/clf-small-grid_ay.csv')
```

```python
#Look at highest precision across models
clf_14 = clf_df[(clf_df['split']==6) & (clf_df['threshold']==14)]
clf_14.style.apply(
    find_best_model.highlight_max, color='darkorange', subset=['precision','f1','auc','recall',
                                                              'auc','accuracy'])

```

```python
#Create df with the max values for each model at threshold 14%, for each split
clf_max_df = clf_df[clf_df['threshold']==14].drop(['parameters'],axis=1)
clf_max_df['max_f1'] = clf_max_df.groupby(['classifier','split','threshold'])['f1'].transform('max')
clf_max_df['max_precision'] = clf_max_df.groupby(['classifier','split','threshold'])['precision'].transform('max')
clf_max_df['max_auc'] = clf_max_df.groupby(['classifier','split','threshold'])['auc'].transform('max')
clf_max_df['max_recall'] = clf_max_df.groupby(['classifier','split','threshold'])['recall'].transform('max')
clf_max_df['max_accuracy'] = clf_max_df.groupby(['classifier','split','threshold'])['accuracy'].transform('max')
clf_max_df.drop(['accuracy','auc','f1','precision','recall'],axis=1,inplace=True)
clf_max_df = clf_max_df.drop_duplicates()
```

```python
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(20)

for key, grp in clf_max_df.groupby(['classifier']):
    ax = grp.plot(ax=ax, kind='line', x='split', y='max_precision', label=key)

plt.Axes.set_xticklabels(ax, [2010, 2011, 2012, 2013, 2014, 2015])
plt.gca().set_ylim([0,1])
plt.title('Best precision by split and model type',fontsize=18)
plt.xlabel('Year of eviction predicted',fontsize=14)
plt.ylabel('Precision Value at 14%',fontsize=14)
```

```python
# Create df to look at highest performing model within gradient boosting

clf_gb = clf_df[clf_df['classifier']=='GB']
clf_gb = clf_gb[clf_gb['threshold']==14]

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(20)

for key, grp in clf_gb.groupby(['parameters']):
    ax = grp.plot(ax=ax, kind='line', x='split', y='precision', label=key)

plt.Axes.set_xticklabels(ax, [2010, 2011, 2012, 2013, 2014, 2015])
plt.gca().set_ylim([0,1])
plt.title('Precision by split for GB models',fontsize=18)
plt.xlabel('Year of eviction predicted',fontsize=14)
plt.ylabel('Precision Value at 14%',fontsize=14)
```

## Regression output analysis

```python
reg_16 = reg_df[reg_df['split']==6]
reg_16.style.apply(
    find_best_model.highlight_min, color='darkorange', subset=['root_mean_squared_error',
                                                              'mean_squared_error'])
#reg_16.style.apply(
    #find_best_model.highlight_max, color='darkorange', subset=['r2',
                                                         #     'explained_variance'])

```

```python
#Create df with the max values for each model for each split
reg_max_df = reg_df.drop(['parameters'],axis=1)
reg_max_df['max_r2'] = reg_max_df.groupby(['classifier','split'])['r2'].transform('max')
reg_max_df['max_explained_var'] = reg_max_df.groupby(['classifier','split'])['explained_variance'].transform('max')
reg_max_df['min_rmse'] = reg_max_df.groupby(['classifier','split'])['root_mean_squared_error'].transform('min')
reg_max_df['min_mean_squared_error'] = reg_max_df.groupby(['classifier','split'])['mean_squared_error'].transform('min')
reg_max_df.drop(['explained_variance','r2','mean_squared_error','root_mean_squared_error'],axis=1,inplace=True)
reg_max_df = reg_max_df.drop_duplicates()
```

```python
# Plot best RMSE over time for each model
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(20)

for key, grp in reg_max_df.groupby(['classifier']):
    ax = grp.plot(ax=ax, kind='line', x='split', y='min_rmse', label=key)

plt.Axes.set_xticklabels(ax, [2010, 2011, 2012, 2013, 2014, 2015])
plt.title('Best (lowest) RMSE by split and model type',fontsize=18)
plt.xlabel('Year of eviction predicted',fontsize=14)
plt.ylabel('RMSE',fontsize=14)
```

# Interpretation of Best Models
Our baseline is a Logistic Regression classifier with a single feature
(evictions the previous year) and the default parameters.

Our best classifier is a Gradient Boosting with the following parameters:
'learning_rate': 0.05, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5.
Our best regressor is a Decision Tree with the following parameters:
'max_depth': 50, 'max_features': None, 'min_samples_split': 10.

This notebook produces additional deliverables upon selecting these models.
This includes the following:

For the baseline classifier:
- A "stump" one-level decision tree ('stump.png')``
- The list of the top 14% of selected blocks ('baseline_selected_blocks.csv')
- The precision-recall curves ('baseline_pr_curve.png')

For the best classifier:
- The list of the top 14% selected blocks ('clf_selected_blocks.csv')
- The list of feature importance ('clf_feature_importance.csv')
- The precision-recall curves ('clf_pr_curve.png')

For the best regressor:
- The list of the top 14% selected blocks ('reg_selected_blocks.csv')
- The list of feature importance ('reg_feature_importance.csv')

And to compare the best classifier and best regressor:
- The list of the top 14% blocks based on actual evictions, and the predictions
  yielded from the best classifier and best regressor for these blocks
  ('clf_reg_comparison.csv')

## Environment Setup

```python
from os import path
from IPython.display import Image
import pipeline
from pipeline import clean

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')
```

## Pipeline Setup

```python
df = pd.read_csv('data/final_merged_df.csv')
splits = pipeline.split_all_years(df, colname='year_evictions')
cleaned_splits = [pipeline.clean_split(split) for split in splits]
labeled_splits = [pipeline.label(split, lower_bound=15, drop_column=True)
                  for split in cleaned_splits]

test_year = 2016
splits_dict = {2011:0, 2012:1, 2013:2, 2014:3, 2015: 4, 2016: 5}
train_df, test_df = labeled_splits[splits_dict[test_year]]
```

## Baseline Classifier
Logistic Regression classifier with a single feature (evictions the previous year) and the default parameters.

```python
params = {}
baseline_model, baseline_scores = pipeline.run_one_clf(
    train_df, test_df, 'LB', params, col_blacklist=['GEOID', 'year_evictions'])
```

#### "Stump" Decision Tree

```python
params = {'max_depth': 1}
dtree, dtree_scores = pipeline.run_one_clf(
    train_df, test_df, 'DT', params, col_blacklist=['GEOID', 'year_evictions'])
analyze_best_model.plot_tree(dtree, test_df, 'stump.png', test_year )
Image(filename=path.join('results', str(test_year), 'stump.png'))
```

#### Selected Blocks

```python
selected_blocks = analyze_best_model.select_k_blocks(baseline_scores, .14 , ['score'], ['GEOID'])
selected_blocks.to_csv(path.join('results', str(test_year), 'baseline_selected_blocks.csv'), index=False)
selected_blocks.head(10)
```

#### Precision-Recall Curves

```python
pipeline.plot_precision_recall_n(
    baseline_scores, .14, 'Precision-Recall: Baseline Classifier', 'baseline_pr_curve.png', test_year)
```

## Best Classifier
Gradient Boosting with the following parameters: 'learning_rate': 0.05, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5.

```python
params = {'learning_rate': 0.05, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5}
best_clf, clf_scores = pipeline.run_one_clf(
    train_df, test_df, 'GB', params, col_blacklist=['GEOID', 'year_evictions'])
```

#### Selected Blocks

```python
selected_blocks = analyze_best_model.select_k_blocks(clf_scores, .14 , ['score'], ['GEOID'])
selected_blocks.to_csv(path.join('results', str(test_year), 'clf_selected_blocks.csv'), index=False)
selected_blocks.head(10)
```

#### Precision-Recall Curves

```python
pipeline.plot_precision_recall_n(
    clf_scores, .14, 'Precision-Recall: Best Classifier', 'clf_pr_curve.png', test_year)
```

#### Feature Importance

```python
importance = analyze_best_model.feature_importance(best_clf, test_df.columns)
importance.to_csv(path.join('results', str(test_year), 'clf_feature_importance.csv'), index=False)
importance.head(10).round(2)
```

## Best Regressor
Decision Tree with the following parameters: 'max_depth': 50, 'max_features':
None, 'min_samples_split': 10.

```python
train_df, test_df = cleaned_splits[splits_dict[test_year]]
params = {'max_depth': 50, 'max_features': None, 'min_samples_split': 10}
best_reg, reg_scores = pipeline.run_one_reg(
    train_df, test_df, 'DTR', params, col_blacklist=['GEOID', 'year_evictions'])
```

#### Selected Blocks

```python
selected_blocks = analyze_best_model.select_k_blocks(reg_scores, .14 , ['pred_evictions'], ['GEOID'])
selected_blocks.to_csv(path.join('results', str(test_year), 'reg_selected_blocks_clf.csv'), index=False)
selected_blocks.head(10)
```

#### Feature Importance

```python
importance = analyze_best_model.feature_importance(best_reg, test_df.columns)
importance.to_csv(path.join('results', str(test_year), 'reg_feature_importance.csv'), index=False)
importance.head(10).round(2)
```

## Comparing Best Classifier and Best Regressor

```python
comparison = analyze_best_model.clf_reg_comparison(
    best_clf, clf_scores, best_reg, reg_scores, test_df, .14)
comparison.to_csv(path.join('results', str(test_year), 'clf_reg_comparison.csv'), index=False)
comparison.head(10).round(2)
```

# Bias and Fairness
## Setup
```python
import numpy as np
from pipeline import BiasCop

df = pd.read_csv('data/final_merged_df.csv')

splits = pipeline.split_last_year(df, colname='year_evictions')
cleaned_splits = [pipeline.clean_split(split) for split in splits]

labeled_splits = [pipeline.label(split, lower_bound=14, drop_column=False)
                  for split in cleaned_splits]

train_df, test_df = labeled_splits[-1]
```

## Classifier Model
```python
params = {'learning_rate': 0.05, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5}
clf_pred_df = pipeline.run_one_clf(
    train_df,
    test_df,
    'GB',
    params,
    col_blacklist=['GEOID', 'year_evictions', 'evictions']
)

clf_cop = BiasCop(clf_pred_df)
clf_cop.xtabs()
```
```python
clf_cop.plot_group_metric('fnr')
```
```python
clf_cop.plot_disparity('fnr_disparity')
```
```python
clf_cop.plot_fairness('for')
```

## Regression Model
```python
params = {'max_depth': 50, 'max_features': None, 'min_samples_split': 10}
reg_pred_df = pipeline.run_one_reg(
    train_df,
    test_df,
    'DTR',
    params,
    label_col='evictions',
    col_blacklist=['GEOID', 'year_evictions', 'label']
)

# Have to turn our predicted scores into a binary label
reg_pred_df = pipeline.label_df(
    reg_pred_df,
    14,
    label_col='pred_label',
    evictions_col='score'
)

reg_cop = BiasCop(reg_pred_df, score_col='pred_label')
reg_cop.xtabs()
```
```python
reg_cop.plot_group_metric('fnr')
```
```python
reg_cop.plot_disparity('fnr_disparity')
```
```python
reg_cop.plot_fairness('fnr')
```
```python
reg_cop.plot_fairness('for')
```
