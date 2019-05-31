import pandas as pd
import sklearn.metrics as metrics

class Evaluator:
    """
    A class that wraps a model's prediction results and can be used to generate
    various metrics based on a threshold.
    """
    def __init__(self, y_predict, y_actual, threshold_percentage):
        self.df = pd.DataFrame({ 'predict': y_predict, 'actual': y_actual })
        self.df = self.df.sort_values('predict', ascending=False)
        self.threshold_percentage = threshold_percentage


class ClassifierEvaluator(Evaluator):
    def prevalence(self):
        """Returns the ratio of actually true outcomes to total outcomes."""
        count_true = len(self.df[self.df.actual == 1])
        return count_true / len(self.df)


    def accuracy(self):
        return metrics.accuracy_score(self.df.actual.values,
                                      self._threshold_labels())


    def precision(self):
        return metrics.precision_score(self.df.actual.values,
                                       self._threshold_labels())


    def recall(self):
        return metrics.recall_score(self.df.actual.values,
                                    self._threshold_labels())


    def f1(self):
        return metrics.f1_score(self.df.actual.values,
                                self._threshold_labels())


    def auc(self):
        return metrics.roc_auc_score(self.df.actual.values,
                                     self._threshold_labels())


    def _threshold_labels(self):
        # Stolen from Rayid Ghani
        # DataFrame must be sorted by predicted score!!!!
        cutoff_index = int(len(self.df) * (self.threshold_percentage / 100.0))
        return [1 if i < cutoff_index else 0 for i in range(len(self.df))]
