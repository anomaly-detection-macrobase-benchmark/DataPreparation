import sys

from sklearn.metrics import average_precision_score

sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser
from utils.fs import load_csv, load_json
import os

arg_parser = ArgParser(
    description='''Evaluates benchmark execution results''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Example:
evaluate.py output/result.json
evaluate.py output/result.json --label is_anomaly --data-dir datasets
evaluate.py output''')
arg_parser.add_argument('path', type=str, help='path to the JSON file or dir with JSON files')
arg_parser.add_argument('--data-dir', type=str, help='path to the directory with the datasets')
arg_parser.add_argument('--label', metavar='COLUMN', dest='label_column_name', default='is_anomaly', type=str,
                        help='label column name (default is_anomaly)')
args = arg_parser.parse_args()


def evaluate(file_path):
    result = load_json(file_path)

    result_dir = os.path.dirname(file_path)

    scores = load_csv(os.path.join(result_dir, result['result']['algorithmOutputFilePath']))['_OUTLIER'].values
    dataset = load_csv(os.path.join(args.data_dir, result['config']['dataset']['id']))
    labels = dataset[args.label_column_name].values

    print('PR AUC: %.2f' % average_precision_score(labels, scores))


if os.path.isdir(args.path):
    file_paths = [os.path.join(args.path, f) for f in os.listdir(args.path) if f.endswith('.json')]
    file_paths = sorted(file_paths, key=lambda f: os.path.getmtime(f))
    for file_path in file_paths:
        print(file_path)
        evaluate(file_path)
        print()
else:
    evaluate(args.path)
