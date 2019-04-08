import sys

sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
from utils.argparse import ArgParser


arg_parser = ArgParser(
    description='''Convert Mulcross DAT file to CSV format''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Example:
mulcross2csv.py MULCROSS.DAT output/mulcross.csv''')
arg_parser.add_argument('file', type=str, help='path to the Mulcross DAT file')
arg_parser.add_argument('output_file', type=str, help='path to the output CSV file')
args = arg_parser.parse_args()

with open(args.file, 'r') as mulcross_file:
    mulcross_file.readline()  # skip
    with open(args.output_file, 'w') as csv_file:
        header_written = False
        for line in mulcross_file:
            parts = line.split()
            if not header_written:
                columns = ['d%d' % i for i in range(1, len(parts) + 1)]
                if parts[-1] in ('0', '1'):
                    columns[-1] = 'is_anomaly'
                csv_file.write(','.join(columns) + '\n')
                header_written = True
            csv_line = ','.join(parts)
            csv_file.write(csv_line + '\n')
