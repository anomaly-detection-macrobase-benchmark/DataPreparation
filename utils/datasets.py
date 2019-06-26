import os
from collections import namedtuple

import pandas as pd

from utils.fs import load_csv

Dataset = namedtuple('Dataset', ['id', 'stats', 'labels'])
DatasetStats = namedtuple('DatasetStats', ['row_count', 'column_count', 'anomaly_count', 'columns'])


def load_stats(df: pd.DataFrame, label_column_name='is_anomaly') -> DatasetStats:
    col_stats = df.describe(include='all')
    anomaly_count = None
    if label_column_name in df:
        label_column = df[label_column_name]
        anomaly_count = label_column.value_counts()[1]
    return DatasetStats(row_count=df.shape[0],
                        column_count=df.shape[1] - (1 if label_column_name else 0),
                        columns=col_stats,
                        anomaly_count=anomaly_count
                        )


def load_dataset(dataset_id, dir_path='', label_column_name='is_anomaly') -> Dataset:
    df = load_csv(os.path.join(dir_path, dataset_id))

    labels = None
    if label_column_name in df:
        labels = df[label_column_name]

    return Dataset(id=dataset_id,
                   stats=load_stats(df, label_column_name),
                   labels=labels)


def load_column(csv_path, column_name):
    df = load_csv(csv_path, [column_name])
    return df[column_name].values
