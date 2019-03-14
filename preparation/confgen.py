import sys
sys.path.insert(0, '..')  # cannot include utils otherwise, not sure if there is better way

import argparse
import os
from utils.argparse import ArgParser
from utils.fs import load_yaml, file_name_without_ext, save_yaml

arg_parser = ArgParser(
    description='''Generates benchmark configs''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:
output/configs --uri csv://dataset.csv --metrics d1,d2,d3,d4,d5,d6,d7,d8,d9 --label is_anomaly --algorithms iforest,mcod,lof-bkaluza,mcd,random --algorithms-config configs/default_algorithms.yaml''')
arg_parser.add_argument('output_dir', type=str, help='path to the dir where the configs will be created')
arg_parser.add_argument('--uri', type=str, required=True, help='dataset path that will be written to the configs')
arg_parser.add_argument('--metrics', metavar='COLUMNS', dest='metric_column_names', type=lambda s: s.split(','),
                        required=True, help='metric column names')
arg_parser.add_argument('--label', metavar='COLUMN', dest='label_column_name', type=str, help='label column name')
arg_parser.add_argument('--algorithms', dest='included_algorithms', type=lambda s: s.split(','),
                        required=True, help='IDs of the algorithms that will be included')
arg_parser.add_argument('--algorithms-config', metavar='FILE', dest='algorithms_config_file',
                        type=str, required=True, help='file with parameters of the ualgorithms')
args = arg_parser.parse_args()

algorithms = {k: v for k, v in load_yaml(args.algorithms_config_file)['algorithms'].items() if k in args.included_algorithms}

for alg_id, params in algorithms.items():
    config_file_path = os.path.join(args.output_dir, '%s_%s.yaml' % (file_name_without_ext(args.uri), alg_id))
    print(config_file_path)
    conf = {
        'dataset': {
            'uri': args.uri,
            'metricColumns': args.metric_column_names
        },
        'algorithm': {
            'id': alg_id,
            'parameters': params
        }
    }
    if args.label_column_name:
        conf['dataset']['labelColumn'] = args.label_column_name
    save_yaml(conf, config_file_path)

