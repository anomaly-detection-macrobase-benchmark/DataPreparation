from collections import namedtuple

import pandas as pd

DatasetStats = namedtuple('DatasetStats', ['row_count', 'column_count', 'anomaly_count', 'columns'])


def load_stats(df: pd.DataFrame, label_column_name=None) -> DatasetStats:
    col_stats = df.describe(include='all')
    anomaly_count = None
    if label_column_name:
        label_column = df[label_column_name]
        anomaly_count = label_column.value_counts()[1]
    return DatasetStats(row_count=df.shape[0],
                        column_count=df.shape[1] - (1 if label_column_name else 0),
                        columns=col_stats,
                        anomaly_count=anomaly_count
                        )
