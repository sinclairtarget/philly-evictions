import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import * 

from sklearn.tree import DecisionTreeClassifier

def plot_precision_recall_n(model, params, train_df, test_df, label):
    X_train = train_df.drop(columns=['GEOID', 'year_evictions', label])
    X_test = test_df.drop(columns=['GEOID', 'year_evictions', label])
    y_train = train_df[label]
    y_test = test_df[label]

    model.set_params(**params)
    model.fit(X_train, y_train)
    pred_scores = model.predict_proba(X_test)[:,1]

    y_true = y_test
    y_prob = pred_scores

    print(y_true.mean())

    from sklearn.metrics import precision_recall_curve
    y_score = y_prob
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score>=value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)
    
    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(pct_above_per_thresh, precision_curve, 'b')
    ax1.set_xlabel('percent of population')
    ax1.set_ylabel('precision', color='b')
    ax2 = ax1.twinx()
    ax2.plot(pct_above_per_thresh, recall_curve, 'r')
    ax2.set_ylabel('recall', color='r')
    ax1.set_ylim([0,1])
    ax2.set_xlim([0,1])
    plt.show()


def top_k_blocks_clf(model, params, train_df, test_df, label, k): 
    X_train, X_test, y_train, y_test = split_dfs(train_df, test_df, label)
    model.set_params(**params)
    model.fit(X_train, y_train)
    pred_scores = model.predict_proba(X_test)[:,1]
    test_df['pred_scores'] = pred_scores
    test_df.sort_values(by='pred_scores', ascending=False, inplace=True)
    top_16 = test_df.head(int(test_df.shape[0]*k)//1)
    return top_16[['GEOID', 'label', 'pred_scores']]


def top_k_blocks_reg(model, params, train_df, test_df, label, k): 
    X_train, X_test, y_train, y_test = split_dfs(train_df, test_df, label)
    model.set_params(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    test_df['preds'] = preds
    test_df.sort_values(by='preds', ascending=False, inplace=True)
    top_16 = test_df.head(int(test_df.shape[0]*k)//1)
    return top_16[['GEOID', 'evictions', 'preds']]


def feature_importance_clf(model, params, train_df, test_df, label): 
    X_train, X_test, y_train, y_test = split_dfs(train_df, test_df, label)
    model.set_params(**params)
    model.fit(X_train, y_train)    
    feature_importance = pd.DataFrame(zip(X_test.columns, model.feature_importances_), 
                                      columns=['feature', 'importance'])
    feature_importance.sort_values(by='importance', ascending=False, inplace=True)
    return feature_importance


def feature_importance_reg(model, params, train_df, test_df, label): 
    X_train, X_test, y_train, y_test = split_dfs(train_df, test_df, label)
    model.set_params(**params)
    model.fit(X_train, y_train)  

    feature_importance = pd.DataFrame(zip(X_test.columns, model.coef_), 
                                      columns=['feature', 'coef'])
    feature_importance['absv_coef'] = feature_importance['coef'].abs()
    feature_importance.sort_values(by='absv_coef', ascending=False, inplace=True)
    return feature_importance


def split_dfs(train_df, test_df, label): 
    X_train = train_df.drop(columns=['GEOID', 'year_evictions', label])
    X_test = test_df.drop(columns=['GEOID', 'year_evictions', label])
    y_train = train_df[label]
    y_test = test_df[label]
    return X_train, X_test, y_train, y_test     


