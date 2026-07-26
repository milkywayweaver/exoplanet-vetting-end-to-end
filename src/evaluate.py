from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,precision_score,f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def evaluate_metrics(y,preds,binary=True):
    '''
    Evaluate metrics given true labels and predicted labels.
    If problem is binary, returns accuracy, recall, precision, and f1 score.
    If multiclass, only returns accuracy.

    Args:
        y (np.ndarray): Array of true labels.
        preds (np.ndarray): Array of predicted labels.
        binary (bool, default=True): Whether the problem is binary problem or not.
    Returns:
        Dictionary of the resulting metrics. 
    '''
    acc = accuracy_score(y,preds)
    metrics = {'accuracy':acc}
    if binary:
        recall = recall_score(y,preds)
        precision = precision_score(y,preds)
        f1 = f1_score(y,preds)
        metrics['recall'] = recall
        metrics['precision'] = precision
        metrics['f1'] = f1

    return metrics

def plot_confmat(y,preds,class_label=None):
    '''
    Plots confusion matrix given true labels and predicted labels.

    Args:
        y (np.ndarray): Array of true labels.
        preds (np.ndarray): Array of predicted labels.
        class_label (list, default=None): Class labels to use for tick labels.
    Returns:
        None        
    '''
    confmat = confusion_matrix(y,preds)
    label = class_label if class_label else np.arange(np.unique(y))
    sns.heatmap(confmat,annot=True,fmt='d',cmap='viridis',xticklabels=label,yticklabels=label)
    plt.xlabel('Predicted')
    plt.ylabel('True')



    
