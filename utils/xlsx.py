from openpyxl.styles import NamedStyle, Font
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows


def cell_value_to_text(value):
    if value is None:
        return ""
    return str(value)


def autofit(sheet):
    for column_cells in sheet.columns:
        col = column_cells[0].column
        length = max(len(cell_value_to_text(cell.value)) for cell in column_cells)
        sheet.column_dimensions[get_column_letter(col)].width = length


def append_blank_rows(sheet, count):
    for _ in range(count):
        sheet.append([])


def append_blank_row(sheet):
    append_blank_rows(sheet, 1)


def pandas_dataframe_to_rows(df, index=True, header=True):
    df_rows = list(dataframe_to_rows(df, index=index, header=header))
    if index:
        df_rows.pop(1)  # there is an empty row, but apparently it's not a bug https://groups.google.com/forum/#!topic/openpyxl-users/N9QpvfzkJIM
    return df_rows


def add_common_styles(workbook):
    workbook.add_named_style(NamedStyle('bold', font=Font(bold=True)))