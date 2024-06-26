import pandas as pd
import numpy as np
import duckdb
from functions import get_file_name
import streamlit as st


class Excel:
    def __init__(self):
        self.data = dict()
        self.xls = None

    def parse_sheet(self, file_name, sheet):
        self.xls: pd.ExcelFile
        sheet_name = sheet.replace('  ', ' ').replace(' ', '_').lower()
        df = self.xls.parse(sheet, encoding='utf-8').replace(np.nan, value='', regex=True)
        df = df.applymap(lambda x: x.replace('\ufeff', '').replace('`', '').strip() if type(x) is str else int(x) if type(x) is float else x)
        df.drop_duplicates()
        df.columns = [c.replace('  ', ' ').replace(' ', '_').lower() for c in df]

        self.data[file_name][sheet_name] = df

    def parse_file(self, excel_file):
        file_name = get_file_name(excel_file)
        self.xls = pd.ExcelFile(excel_file)

        if file_name not in self.data.keys():
            self.data[file_name] = dict()
        for sheet in self.xls.sheet_names:
            self.parse_sheet(file_name, sheet)


@st.cache_data
def read_excel(file_path):
    print("#####12345")
    df_dict = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')  # Load all sheets
    return df_dict


def load_excel_to_duckdb(file_path):
    df_dict = read_excel(file_path)
    file_name = file_path.name.split(".")[0]
    con = duckdb.connect(database=f'{file_name}.duckdb')
    sheet_info = {}

    for sheet_name, data in df_dict.items():
        try:
            # Convert all columns to string to avoid type issues
            data = data.astype(str)

            # remove spaces from column name
            data.columns = [str(c).replace('  ', ' ').replace(' ', '_').lower() for c in data]

            # remove spaces from sheet_name
            sheet_name = sheet_name.replace('  ', ' ').replace(' ', '_').lower()
            con.execute(f"drop TABLE if exists {sheet_name}")
            con.execute(f"CREATE TABLE {sheet_name} AS SELECT * FROM data")
            sheet_info[sheet_name] = list(data.columns)
        except Exception as e:
            print(f"Error loading sheet {sheet_name}: {e}, {data.columns}")

    return con, sheet_info
