import itertools
from operator import itemgetter
import argparse
from evaluation.common import load_execution_result, pr_auc
from utils.argparse import ArgParser
from utils.fs import file_name_without_ext
from utils.plots import marker_cycle, color_cycle, save_plot
import matplotlib.pyplot as plt
import os
import numpy as np

arg_parser = ArgParser(
    description='''Evaluates algorithms quality on different datasets''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:''')
arg_parser.add_argument('result_dir', type=str, help='path to the directory with the benchmark result')
arg_parser.add_argument('--data-dir', type=str, help='path to the directory with the datasets')
arg_parser.add_argument('--title', type=str, help='title displayed on the plots')
arg_parser.add_argument('--output-dir', type=str, help='path to the directory for saving plots')
arg_parser.add_argument('--silent', action='store_true', help='do not show plots')
args = arg_parser.parse_args()

results_file_paths = [os.path.join(args.result_dir, f) for f in os.listdir(args.result_dir) if f.endswith('.json')]

execution_results = [load_execution_result(f, include_scores=True, result_dir=args.result_dir, include_labels=True)
                     for f in results_file_paths]
execution_results.sort(key=itemgetter('algorithm'))

algorithm_results = {id: sorted(list(g), key=lambda x: x['dataset'])
                     for id, g in itertools.groupby(execution_results, lambda item: item['algorithm'])}


def clean_dataset_name(s):
    return file_name_without_ext(s)\
        .replace('unsupervised-ad-', '')\
        .replace('-ann-test', '')\
        .replace('-sub', '')\
        .replace('-onehot', '')\
        .replace('quality-white', '')\
        .replace('.tst', '')


dataset_id = {r['dataset'] for r in execution_results}
dataset_names = [clean_dataset_name(name) for name in sorted(dataset_id)]
xticks_values = np.arange(0, len(dataset_names), 1)

fig = plt.figure(figsize=[9, 5])
fig.subplots_adjust(bottom=0.2) # or whatever
plt.suptitle(args.title)
color = color_cycle()
marker = marker_cycle()


for alg_id, g in algorithm_results.items():
    plt.plot(xticks_values, [pr_auc(it['scores'], it['labels']) for it in g],
             label=alg_id, color=next(color), marker=next(marker))
plt.xticks(xticks_values, dataset_names, rotation=30)
plt.legend(loc='upper left')
plt.xlabel('dataset')
plt.ylabel('PR AUC')
plt.grid()

if args.output_dir:
    save_plot(fig, 'auc', args.output_dir)

if not args.silent:
    plt.show()
