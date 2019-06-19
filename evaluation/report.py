import argparse
import os

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from utils.argparse import ArgParser
from utils.datasets import load_stats
from utils.fs import load_json, load_csv, list_files
from utils.xlsx import autofit, append_blank_rows

arg_parser = ArgParser(
    description='''Generates a report.''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:
report.py ../../macrobase/alexp/output output/report.xlsx --data-dir ../../datasets''')
arg_parser.add_argument('result_dir', type=str, help='path to the directory with the benchmark result')
arg_parser.add_argument('output_file', type=str, help='path to the output file (Excel .xlsx)')
arg_parser.add_argument('--data-dir', type=str, help='path to the directory with the datasets')
args = arg_parser.parse_args()

results_file_paths = [f for f in list_files(args.result_dir) if f.endswith('.json')]

execution_results = [load_json(f) for f in results_file_paths]

data_file_ids = {r['config']['dataset']['id'] for r in execution_results}

workbook = Workbook()
workbook.remove(workbook.active)  # remove default sheet


def write_datasets_sheet():
    sheet = workbook.create_sheet('Datasets')

    stats_dict = {}
    for data_file_id in data_file_ids:
        dataset = load_csv(os.path.join(args.data_dir, data_file_id))
        stats = load_stats(dataset, 'is_anomaly')
        stats_dict[data_file_id] = stats

    # main stats table
    sheet.append(['Samples', 'Dims', '% anomalies'])
    for data_file_id, stats in stats_dict.items():
        sheet.append([data_file_id, stats.row_count, stats.column_count, stats.anomaly_count / stats.row_count * 100])

    # column stats for each dataset
    for data_file_id, stats in stats_dict.items():
        append_blank_rows(sheet, 2)

        sheet.append([data_file_id])
        col_stats: pd.DataFrame = stats.columns
        df_rows = list(dataframe_to_rows(col_stats, index=True, header=True))
        df_rows.pop(1)  # https://groups.google.com/forum/#!topic/openpyxl-users/N9QpvfzkJIM
        for r in df_rows:
            sheet.append(r)

    autofit(sheet)


def write_algorithms_sheet():
    sheet = workbook.create_sheet('Algorithms')


write_datasets_sheet()
write_algorithms_sheet()

workbook.save(args.output_file)
