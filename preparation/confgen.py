import argparse
import os
from utils.argparse import ArgParser
from utils.fs import load_yaml, file_name_without_ext, save_yaml

arg_parser = ArgParser(
    description='''Generates benchmark configs''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples:
output/configs --uri csv://dataset.csv --metrics d1,d2,d3,d4,d5,d6,d7,d8,d9 --label is_anomaly --algorithms iforest,mcod,lof-bkaluza,mcd,random --algorithms-config configs/default_algorithms.yaml
output/configs --dataset-config configs/datasets/shuttle-goldstein.yaml --algorithms iforest,mcod,lof-bkaluza,mcd,random --algorithms-config configs/default_algorithms.yaml''')
arg_parser.add_argument('output_dir', type=str, help='path to the dir where the configs will be created')
arg_parser.add_argument('--uri', type=str, help='dataset path that will be written to the configs')
arg_parser.add_argument('--metrics', metavar='COLUMNS', dest='metric_column_names', type=lambda s: s.split(','),
                        help='metric column names')
arg_parser.add_argument('--label', metavar='COLUMN', dest='label_column_name', type=str, help='label column name')
arg_parser.add_argument('--algorithms', dest='included_algorithms', type=lambda s: s.split(','),
                        required=True, help='IDs of the algorithms that will be included')
arg_parser.add_argument('--algorithms-config', metavar='FILE', dest='algorithms_config_file',
                        type=str, required=True, help='file with parameters of the algorithms')
arg_parser.add_argument('--dataset-config', metavar='FILE', dest='dataset_config_file', type=str,
                        help='file with the dataset config, instead of --uri, --metrics, --label args (still can be used to override)')
args = arg_parser.parse_args()

algorithms = {k: v for k, v in load_yaml(args.algorithms_config_file)['algorithms'].items() if k in args.included_algorithms}

file_dataset_conf = load_yaml(args.dataset_config_file) if args.dataset_config_file else {}
args_dataset_conf = {
    'uri': args.uri,
    'metricColumns': args.metric_column_names,
    'labelColumn': args.label_column_name
}
args_dataset_conf = {k:v for k,v in args_dataset_conf.items() if v is not None}
dataset_conf = {**file_dataset_conf, **args_dataset_conf}

for alg_id, params in algorithms.items():
    config_file_path = os.path.join(args.output_dir, '%s_%s.yaml' % (file_name_without_ext(dataset_conf['uri']), alg_id))
    print(config_file_path)
    conf = {
        'dataset': dataset_conf,
        'algorithm': {
            'id': alg_id,
            'parameters': params
        }
    }
    save_yaml(conf, config_file_path)
