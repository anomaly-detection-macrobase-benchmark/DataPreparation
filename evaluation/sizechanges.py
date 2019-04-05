import itertools
import sys
from operator import itemgetter

from sklearn.metrics import average_precision_score

sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser
from utils.fs import load_csv, load_json
from utils.plots import marker_cycle, color_cycle, save_plot
import matplotlib.pyplot as plt
import os

arg_parser = ArgParser(
    description='''Evaluates algorithms robustness, time, memory when increasing dataset sizes''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:''')
arg_parser.add_argument('result_dir', type=str, help='path to the directory with the benchmark result')
arg_parser.add_argument('--data-dir', type=str, help='path to the directory with the datasets')
arg_parser.add_argument('--label', metavar='COLUMN', dest='label_column_name', type=str, help='label column name')
arg_parser.add_argument('--title', type=str, help='title displayed on the plots')
arg_parser.add_argument('--scale', type=str, default='linear', help='plot axis scale, linear or log')
arg_parser.add_argument('--output-dir', type=str, help='path to the directory for saving plots')
arg_parser.add_argument('--silent', action='store_true', help='do not show plots')
args = arg_parser.parse_args()

results_file_paths = [os.path.join(args.result_dir, f) for f in os.listdir(args.result_dir) if f.endswith('.json')]

results = [load_json(f) for f in results_file_paths]

execution_results = [{
    'trainingTime': r['result']['trainingTime'],
    'classificationTime': r['result']['classificationTime'],
    'maxMemory': r['result']['maxMemory'],
    'scores': load_csv(os.path.join(args.result_dir, r['result']['algorithmOutputFilePath']))['_OUTLIER'].values,
    'algorithm': r['config']['algorithm']['id'],
    'dataset': r['config']['dataset']['id']
} for r in results]
execution_results.sort(key=itemgetter('algorithm'))

algorithm_results = {id: sorted(list(g), key=lambda x: len(x['scores']))
                     for id, g in itertools.groupby(execution_results, lambda item: item['algorithm'])}


def has_training(group):
    return any(it['trainingTime'] > 0 for it in group)


plt.figure(1, figsize=[14, 5])
plt.suptitle(args.title)

plt.subplot(1, 2, 1)
color = color_cycle()
marker = marker_cycle()
for alg_id, g in algorithm_results.items():
    if not has_training(g):
        next(color)
        next(marker)
        continue
    plt.plot([len(it['scores']) for it in g],
             [it['trainingTime'] for it in g],
             label=alg_id, color=next(color), marker=next(marker))
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('training time')
plt.yscale(args.scale)
plt.xscale(args.scale)

plt.subplot(1, 2, 2)
color = color_cycle()
marker = marker_cycle()
for alg_id, g in algorithm_results.items():
    plt.plot([len(it['scores']) for it in g],
             [it['classificationTime'] for it in g],
             label=alg_id, color=next(color), marker=next(marker))
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('classification time')
plt.yscale(args.scale)
plt.xscale(args.scale)

if args.output_dir:
    save_plot(plt.gcf(), 'time', args.output_dir)
if not args.silent:
    plt.show()

color = color_cycle()
marker = marker_cycle()
plt.suptitle(args.title)
for alg_id, g in algorithm_results.items():
    plt.plot([len(it['scores']) for it in g],
             [it['maxMemory'] / 1024 / 1024 for it in g],
             label=alg_id, color=next(color), marker=next(marker))
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('max memory usage, MB')
plt.yscale(args.scale)
plt.xscale(args.scale)

if args.output_dir:
    save_plot(plt.gcf(), 'memory', args.output_dir)
if not args.silent:
    plt.show()

if not args.label_column_name:
    exit(0)


def pr_auc(scores, labels):
    return average_precision_score(labels, scores)


data_file_ids = {r['config']['dataset']['id'] for r in results}
datasets = {id: load_csv(os.path.join(args.data_dir, id)) for id in data_file_ids}

labels = {id: d[args.label_column_name].values for id, d in datasets.items()}

color = color_cycle()
marker = marker_cycle()

for alg_id, g in algorithm_results.items():
    plt.plot([len(it['scores']) for it in g],
             [pr_auc(it['scores'], labels[it['dataset']]) for it in g],
             label=alg_id, color=next(color), marker=next(marker))
plt.legend(loc='upper left')
plt.xlabel('dataset size')
plt.ylabel('PR AUC')
plt.xscale('log')
plt.yscale(args.scale)
plt.xscale(args.scale)
plt.title(args.title)

if args.output_dir:
    save_plot(plt.gcf(), 'auc', args.output_dir)
if not args.silent:
    plt.show()
