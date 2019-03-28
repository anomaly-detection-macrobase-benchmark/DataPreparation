import itertools
import sys
from operator import itemgetter

from sklearn.metrics import average_precision_score

sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser
from utils.fs import load_csv, load_json
import matplotlib.pyplot as plt
import os

arg_parser = ArgParser(
    description='''Evaluates algorithms robustness, time, memory when increasing dataset sizes''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:''')
arg_parser.add_argument('result_dir', type=str, help='path to the directory with the benchmark result')
arg_parser.add_argument('--data-dir', type=str, help='path to the directory with the datasets')
arg_parser.add_argument('--label', metavar='COLUMN', dest='label_column_name', required=True, type=str, help='label column name')
arg_parser.add_argument('--title', type=str, help='title displayed on the plots')
args = arg_parser.parse_args()

results_file_paths = [os.path.join(args.result_dir, f) for f in os.listdir(args.result_dir) if f.endswith('.json')]

results = [load_json(f) for f in results_file_paths]

data_file_ids = {r['config']['dataset']['id'] for r in results}
datasets = {id: load_csv(os.path.join(args.data_dir, id)) for id in data_file_ids}
labels = {id: d[args.label_column_name].values for id, d in datasets.items()}

execution_results = [{
    'timeElapsed': r['result']['timeElapsed'],
    'scores': load_csv(os.path.join(args.result_dir, r['result']['algorithmOutputFilePath']))['_OUTLIER'].values,
    'algorithm': r['config']['algorithm']['id'],
    'dataset': r['config']['dataset']['id']
} for r in results]
execution_results.sort(key=itemgetter('algorithm'))

algorithm_results = {id: sorted(list(g), key=lambda x: len(x['scores']))
                     for id, g in itertools.groupby(execution_results, lambda item: item['algorithm'])}

for id, g in algorithm_results.items():
    plt.plot([len(it['scores']) for it in g],
             [it['timeElapsed'] for it in g],
             label=id)
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('time')
plt.title(args.title)
plt.show()


def pr_auc(scores, labels):
    return average_precision_score(labels, scores)


for id, g in algorithm_results.items():
    plt.plot([len(it['scores']) for it in g],
             [pr_auc(it['scores'], labels[it['dataset']]) for it in g],
             label=id)
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('PR AUC')
plt.show()