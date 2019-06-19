from openpyxl.utils import get_column_letter


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
