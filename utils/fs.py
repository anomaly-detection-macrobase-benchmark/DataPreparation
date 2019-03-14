import os
import pandas as pd
import yaml


def create_dirs_if_not_exist(path):
    os.makedirs(path, exist_ok=True)


def create_dirs_for_file(file_path):
    create_dirs_if_not_exist(os.path.dirname(file_path))


def file_name_without_ext(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def load_csv(file_path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def save_csv(df, file_path):
    create_dirs_for_file(file_path)
    df.to_csv(file_path, index=False)


def load_yaml(file_path) -> dict:
    with open(file_path, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


def save_yaml(data, file_path):
    create_dirs_for_file(file_path)
    with open(file_path, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
