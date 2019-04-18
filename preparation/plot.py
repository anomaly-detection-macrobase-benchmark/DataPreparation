import os
from enum import IntEnum
import argparse
from utils.argparse import ArgParser
from utils.plots import save_plot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils.fs import load_csv, file_name_without_ext

arg_parser = ArgParser(
    description='''Plots 2D dataset''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:
plot.py datasets/mulcross.csv
plote.py datasets/mulcross.csv --label is_anomaly --attr d1,d2
plote.py datasets/mulcross.csv --label is_anomaly --output-dir output/plots --silent
plot.py datasets''')
arg_parser.add_argument('path', type=str, help='path to the CSV file or dir with CSV files')
arg_parser.add_argument('--attr', type=lambda s: s.split(','), help='attributes to be plotted (default the first 2 columns)')
arg_parser.add_argument('--label', metavar='label_column', dest='label_column_name', default='is_anomaly', type=str, help='label column name (default is_anomaly)')
arg_parser.add_argument('--score', metavar='score_column', dest='score_column_name', default='_OUTLIER', type=str, help='score column name (default _OUTLIER)')
arg_parser.add_argument('--threshold', metavar='score_threshold', default=0.5, type=float, help='score threshold (default 0.5)')
arg_parser.add_argument('--title', default='{file_name}', type=str, help='title displayed on the plots')
arg_parser.add_argument('--output-dir', type=str, help='path to the directory for saving plots')
arg_parser.add_argument('--silent', action='store_true', help='do not show plots')
args = arg_parser.parse_args()


class ResultType(IntEnum):
    TRUE_NEGATIVE = 0
    FALSE_NEGATIVE = 1
    TRUE_POSITIVE = 2
    FALSE_POSITIVE = 3

    def pretty_name(self):
        return self.name.lower().replace('_', ' ')


def process(file_path):
    df = load_csv(file_path)
    file_name = file_name_without_ext(file_path)
    attributes = args.attr if args.attr else list(df.columns)[0:2]
    title = args.title.format(file_name=file_name)

    has_labels = args.label_column_name in df
    labels = df[args.label_column_name] if has_labels else [0] * len(df)

    has_scores = args.score_column_name in df
    if has_scores and not has_labels:
        print('Label column not found, cannot use scores')
        has_scores = False
    scores = df[args.score_column_name] if has_scores else [0] * len(df)

    def get_result_type(score, label, threshold):
        if label == 0:
            return ResultType.FALSE_POSITIVE if score > threshold else ResultType.TRUE_NEGATIVE
        return ResultType.TRUE_POSITIVE if score > threshold else ResultType.FALSE_NEGATIVE

    result_color_map = {
        ResultType.TRUE_NEGATIVE: 'royalblue',
        ResultType.FALSE_NEGATIVE: 'red',
        ResultType.TRUE_POSITIVE: 'limegreen',
        ResultType.FALSE_POSITIVE: 'darkorange',
    }

    results = [get_result_type(it[0], it[1], args.threshold) for it in zip(scores, labels)]

    fig = plt.figure()
    plt.suptitle(title)
    plt.scatter(df[attributes[0]], df[attributes[1]], c=[result_color_map[r] for r in results])
    plt.xlabel(attributes[0])
    plt.ylabel(attributes[1])
    if has_scores:
        plt.legend(handles=[mpatches.Patch(color=result_color_map[r], label=r.pretty_name()) for r in set(results)])

    if args.output_dir:
        save_plot(fig, 'data', args.output_dir)


if os.path.isdir(args.path):
    file_paths = [os.path.join(args.path, f) for f in os.listdir(args.path) if f.endswith('.csv')]
    file_paths = sorted(file_paths, key=lambda f: os.path.getmtime(f))
    for file_path in file_paths:
        print(file_path)
        process(file_path)
        print()
else:
    process(args.path)

if not args.silent:
    plt.show()
