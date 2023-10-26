import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, NamedStyle
from openpyxl.utils.dataframe import dataframe_to_rows

def convert_to_excel(filename, data_list):
    output_dir = os.getcwd()
    file_name = os.path.join(output_dir, f"{filename}.xlsx")

    df = pd.DataFrame(data_list)

    writer = pd.ExcelWriter(file_name, engine='openpyxl')

    df.to_excel(writer, sheet_name='Sheet1', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    date_style = NamedStyle(name='date_style')
    date_style.font = Font(bold=True)
    date_style.alignment = Alignment(horizontal='left', vertical='center')

    column_widths = [max(len(str(val)) for val in df[col]) + 2 for col in df.columns]
    for i, width in enumerate(column_widths, 1):
        worksheet.column_dimensions[worksheet.cell(row=1, column=i).column_letter].width = width

    for cell in worksheet['1']:
        cell.style = date_style

    workbook.save(file_name)

    return file_name
