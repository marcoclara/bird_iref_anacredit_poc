import pandas as pd
from sqlalchemy import create_engine
import re

# Configuração da ligação à base de dados PostgreSQL
DB_USER = 'postgres'
DB_PASS = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bird_iref_anacredit_poc_v2'
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Caminho para o ficheiro Excel
excel_path = 'c:/anacredit_example.xlsx'

xls = pd.ExcelFile(excel_path, engine='openpyxl')
sheet_names = [s for s in xls.sheet_names if s.lower().startswith("case")]

def load_blocks():
    all_data = dict()
    for sheet in sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet, header=None, engine='openpyxl')
        current_table = None
        current_columns = None
        for idx, row in df.iterrows():
            table_name = row[0]
            if pd.notna(table_name) and (current_table is None or table_name != current_table):
                current_table = str(table_name).strip().lower().replace(" ", "_")
                current_columns = None
                if current_table not in all_data:
                    all_data[current_table] = []
                continue
            if current_table:
                if current_columns is None:
                    current_columns = row[2:].dropna().tolist()
                    continue
                data_row = row[2:2+len(current_columns)]
                if data_row.isnull().all():
                    current_table = None
                    current_columns = None
                    continue
                record = dict(zip(current_columns, data_row))
                all_data[current_table].append(record)
    return all_data

def clean_column_names(columns):
    return [re.sub(r'\W+', '_', str(c).strip().lower()) for c in columns]

def load_to_postgres(data_dict):
    for table, records in data_dict.items():
        if not records:
            continue
        df = pd.DataFrame(records)
        df.columns = clean_column_names(df.columns)
        df.to_sql(table, engine, if_exists='append', index=False)
        print(f"Tabela {table} carregada com {len(df)} registos.")

if __name__ == '__main__':
    data = load_blocks()
    load_to_postgres(data)

