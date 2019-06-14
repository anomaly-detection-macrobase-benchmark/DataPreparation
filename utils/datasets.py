import pandas as pd


def load_stats(df: pd.DataFrame, label_column_name=None):
    col_stats = df.describe(include='all')
    result = {
        'columns': col_stats,
        'row_count': df.shape[0],
        'column_count': df.shape[1] - (1 if label_column_name else 0)
    }
    if label_column_name:
        label_column = df[label_column_name]
        result['anomaly_percent'] = label_column.value_counts(normalize=True)[1]
    return result
