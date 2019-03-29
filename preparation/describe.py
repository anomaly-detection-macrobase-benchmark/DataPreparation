import sys
sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser
import pandas as pd
from utils.fs import load_csv

arg_parser = ArgParser(
    description='''Prints dataset info''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Example:
describe.py original_datasets/shuttle-unsupervised-ad.csv
describe.py original_datasets/shuttle-unsupervised-ad.csv --label is_anomaly''')
arg_parser.add_argument('file', type=str, help='path to the CSV file')
arg_parser.add_argument('--no-contents', action='store_true', help='do not print element values (head, tail)')
arg_parser.add_argument('--label', metavar='label_column', dest='label_column_name', type=str, help='label column name')
args = arg_parser.parse_args()

df = load_csv(args.file)

pd.set_option('display.max_columns', 500)
pd.options.display.float_format = '{:.6f}'.format
if not args.no_contents:
    print(df)
print(df.describe(include='all'))

if args.label_column_name:
    print('\nLabel column: ')
    label_column = df[args.label_column_name]
    print('Value    %')
    print(label_column.value_counts(normalize=True) * 100)
