import argparse
from utils.argparse import ArgParser
from utils.fs import load_csv, save_csv
import pandas as pd


arg_parser = ArgParser(
    description='''Encodes categorical attributes using one-hot encoding''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Example:
encodecat.py dataset.csv dataset-onehot.csv --columns=type1,type2''')
arg_parser.add_argument('file', type=str, help='path to the input CSV file')
arg_parser.add_argument('output_file', type=str, help='path to the output CSV file')
arg_parser.add_argument('--columns', dest='categorical_column_names', type=lambda s: s.split(','),
                        required=True, help='categorical column names')
args = arg_parser.parse_args()

df = load_csv(args.file)

print('Input size: %s ' % str(df.shape))

for col_name in args.categorical_column_names:
    col = df[col_name]
    encoded_col = pd.get_dummies(col, prefix=col_name)
    df = pd.concat([df, encoded_col], axis=1, sort=False)
    print("Size after encoding '%s': %s, added %s" % (col_name, str(df.shape), encoded_col.columns.values))

save_csv(df, args.output_file)
