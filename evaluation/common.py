import os

from sklearn.metrics import average_precision_score

from utils.fs import load_json, load_csv


def load_execution_result(file_path, include_scores=False, include_labels=False):
    r = load_json(file_path)

    classifier_key = 'algorithm' if 'algorithm' in r['config'] else 'classifier'

    result = {
        'trainingTime': r['result']['trainingTime'],
        'classificationTime': r['result']['classificationTime'],
        'maxMemory': r['result']['maxMemory'],
        'classifier': r['config'][classifier_key]['id'],
        'dataset': r['config']['dataset']['id'],
        'algorithmOutputFilePath': r['result']['algorithmOutputFilePath']
    }
    if include_scores:
        data = load_csv(os.path.join(os.path.dirname(file_path), result['algorithmOutputFilePath']))
        result['scores'] = data['_OUTLIER'].values
        if include_labels:
            result['labels'] = data[r['config']['dataset']['labelColumn']].values
    return result


def pr_auc(scores, labels):
    return average_precision_score(labels, scores)
