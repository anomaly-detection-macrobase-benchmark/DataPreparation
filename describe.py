import argparse
from utils.argparse import ArgParser
import pandas as pd


parser = ArgParser(
    description='''Prints dataset info''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Example:
describe.py output/index.json
describe.py output/index.json --label is_anomaly''')
parser.add_argument('file', type=str, help='path to the CSV file')
parser.add_argument('--label', metavar='label_column', dest='label_column_name', type=str, help='label column name')
args = parser.parse_args()

df = pd.read_csv(args.file, sep=',')

print(df)
pd.set_option('display.max_columns', 500)
print(df.describe(include='all'))

if (args.label_column_name):
    print('\nLabel column: ')
    label_column = df[args.label_column_name]
    print('Value    %')
    print(label_column.value_counts(normalize=True) * 100)
