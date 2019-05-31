import json
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


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_files(path, recursive=True):
    if recursive:
        return [os.path.join(dp, f) for dp, _, fn in os.walk(path) for f in fn]
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
