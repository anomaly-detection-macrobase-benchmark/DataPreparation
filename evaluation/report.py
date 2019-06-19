import argparse
import os

import pandas as pd
import xlsxwriter

from utils.argparse import ArgParser
from utils.datasets import load_stats
from utils.fs import load_json, load_csv, list_files

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

pd_excel_writer = pd.ExcelWriter(args.output_file, engine='xlsxwriter') # use this to simplify Pandas data writing
workbook: xlsxwriter.Workbook = pd_excel_writer.book

bold = workbook.add_format({'bold': True})


def add_worksheet(name):
    worksheet = workbook.add_worksheet(name)
    pd_excel_writer.sheets[worksheet.name] = worksheet
    return worksheet


def write_datasets_sheet():
    worksheet = add_worksheet('Datasets')

    worksheet.set_column(0, 0, 45)
    worksheet.set_column(1, 99, 15)

    summaries = []
    details_row = len(data_file_ids) + 3
    for data_file_id in data_file_ids:
        dataset = load_csv(os.path.join(args.data_dir, data_file_id))
        stats = load_stats(dataset, 'is_anomaly')

        summaries.append([stats.row_count, stats.column_count, stats.anomaly_count / stats.row_count * 100])

        worksheet.write(details_row, 0, data_file_id, bold)
        col_stats: pd.DataFrame = stats.columns
        col_stats.to_excel(pd_excel_writer, sheet_name=worksheet.name, startrow=details_row + 1)
        details_row += col_stats.shape[0] + 3

    summary_df = pd.DataFrame(summaries, columns=['Samples', 'Dims', '% anomalies'], index=data_file_ids)
    summary_df.to_excel(pd_excel_writer, sheet_name=worksheet.name)


def write_algorithms_sheet():
    worksheet = add_worksheet('Algorithms')


write_datasets_sheet()
write_algorithms_sheet()

workbook.close()