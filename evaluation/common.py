import os

from utils.fs import load_json, load_csv


def load_execution_result(file_path, include_scores=False, result_dir=''):
    r = load_json(file_path)

    result = {
        'trainingTime': r['result']['trainingTime'],
        'classificationTime': r['result']['classificationTime'],
        'maxMemory': r['result']['maxMemory'],
        'algorithm': r['config']['algorithm']['id'],
        'dataset': r['config']['dataset']['id'],
        'algorithmOutputFilePath': r['result']['algorithmOutputFilePath']
    }
    if include_scores:
        result['scores'] = load_csv(os.path.join(result_dir, result['algorithmOutputFilePath']))['_OUTLIER'].values
    return result
