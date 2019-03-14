import os

import pandas as pd


def create_dirs_if_not_exist(path):
    os.makedirs(path, exist_ok=True)


def create_dirs_for_file(file_path):
    create_dirs_if_not_exist(os.path.dirname(file_path))


def load_csv(file_path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def save_csv(df, file_path):
    create_dirs_for_file(file_path)
    df.to_csv(file_path, index=False)
