################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import pandas as pd
import re
import os

# Path to original dataset file location
input_file = "anacredit_ecb/input/AnaCredit_Manual_Part_III_Examples_of_complete_reports.xlsx"

# Path to output file location (split per sheet)
output_dir = "anacredit_ecb/output/excel"
os.makedirs(output_dir, exist_ok=True)

# Load all sheets prefixed with "CASE"
xls = pd.ExcelFile(input_file, engine="openpyxl")
sheet_names = [s for s in xls.sheet_names if s.upper().startswith("CASE")]

def limpar_nome_entidade(nome):
    nome_limpo = re.sub(r'\s*dataset\s*$', '', str(nome), flags=re.IGNORECASE).strip()
    return nome_limpo if nome_limpo else "Entidade_Desconhecida"

# Iteration over existing sheets
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, header=None, engine="openpyxl")
    entidades_dict = {}
    current_entidade = None
    current_block = []

    for i, row in df.iterrows():
        entidade_raw = row[0]
        if pd.isna(entidade_raw):
            continue
        entidade = limpar_nome_entidade(entidade_raw)

        if entidade != current_entidade:
            if current_entidade and current_block:
                header = current_block[0]
                data_rows = current_block[1:]
                if current_entidade not in entidades_dict:
                    entidades_dict[current_entidade] = []
                entidades_dict[current_entidade].append((header, data_rows))
            current_entidade = entidade
            filtered_row = row.drop(labels=[0]).tolist()
            current_block = [filtered_row]
        else:
            filtered_row = row.drop(labels=[0]).tolist()
            current_block.append(filtered_row)

    if current_entidade and current_block:
        header = current_block[0]
        data_rows = current_block[1:]
        if current_entidade not in entidades_dict:
            entidades_dict[current_entidade] = []
        entidades_dict[current_entidade].append((header, data_rows))

    output_file = os.path.join(output_dir, f"{sheet}.xlsx")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        sheets_criadas = 0
        for entidade, blocos in entidades_dict.items():
            for header, data in blocos:
                # Correct lines of data to fit same length as header
                header_len = len(header)
                data_corrigida = []
                for linha in data:
                    if len(linha) < header_len:
                        linha = linha + [""] * (header_len - len(linha))
                    elif len(linha) > header_len:
                        linha = linha[:header_len]
                    data_corrigida.append(linha)

                df_entidade = pd.DataFrame(data_corrigida, columns=header)

                sheet_name = re.sub(r'[\\/*?:[\]]', '_', entidade)[:31]
                if not sheet_name:
                    sheet_name = "Entidade_Desconhecida"
                df_entidade.to_excel(writer, sheet_name=sheet_name, index=False)
                sheets_criadas += 1

    print(f"✅ Generated file: {output_file} with {sheets_criadas} entities.")
    