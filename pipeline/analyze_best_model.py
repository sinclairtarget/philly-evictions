from sklearn.metrics import precision_recall_curve
import numpy as np


def plot_precision_recall_n(y_test, y_prob, model_name):
    '''
    CITATION: Leveraged Prof Ghani's magic loop function for plotting precision-recall at thresholds
    
    Plots the precision and recall at different thresholds leveraging sklearn's 
    precision recall function

    Inputs: true label values for the test data set; predicted probability scores from model,
    name of the model 
    '''
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_prob)
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
    ax1.set_ylim([0,1])
    ax2.set_xlim([0,1])
    
    plt.title(model_name)
    plt.savefig('graphs/'+model_name)

def get_feature_importances(model, model_name):
    '''
    Note -- this will work for gradient boosting, decision trees, random forest 
    '''
    feature_scores = model.feature_importances_
    d = {'Features': x_train.columns, "Importance": feature_scores}
    feature_importance = feature_importance.sort_values(by=['Importance'], ascending=False)
    feature_importance.to_csv('features/'+models_to_run[index]+'_'+str(model_num)+'.csv') 

def plot_precision_at_k(y_test, y_prob, model_name):
    '''
    '''