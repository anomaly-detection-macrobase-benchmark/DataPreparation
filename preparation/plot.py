import os
import sys

from matplotlib.colors import ListedColormap

sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser
from utils.plots import save_plot
import matplotlib.pyplot as plt
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
arg_parser.add_argument('--title', default='{file_name}', type=str, help='title displayed on the plots')
arg_parser.add_argument('--output-dir', type=str, help='path to the directory for saving plots')
arg_parser.add_argument('--silent', action='store_true', help='do not show plots')
args = arg_parser.parse_args()


def process(file_path):
    df = load_csv(file_path)
    file_name = file_name_without_ext(file_path)
    attributes = args.attr if args.attr else list(df.columns)[0:2]
    labels = df[args.label_column_name] if args.label_column_name in df else [0] * len(df)
    title = args.title.format(file_name=file_name)

    fig = plt.figure()
    plt.suptitle(title)
    plt.scatter(df[attributes[0]], df[attributes[1]], c=labels, cmap=ListedColormap(['royalblue', 'red']))
    plt.xlabel(attributes[0])
    plt.ylabel(attributes[1])

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
