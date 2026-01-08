import pandas as pd
import re

# Caminho para o ficheiro original
input_file = "ecb_dataset/AnaCredit_Manual_Part_III_Examples_of_complete_reports.xlsx"
output_file = "ecb_dataset/AnaCredit_Entidades_Separadas.xlsx"

# Carregar todas as sheets que começam por "CASE"
xls = pd.ExcelFile(input_file)
sheet_names = [s for s in xls.sheet_names if s.startswith("CASE")]

# Dicionário para armazenar dados por entidade
entidades_dict = {}

def limpar_nome_entidade(nome):
    # Remove o sufixo "dataset" (case insensitive) e espaços extras
    nome_limpo = re.sub(r'\s*dataset\s*$', '', str(nome), flags=re.IGNORECASE).strip()
    return nome_limpo if nome_limpo else "Entidade_Desconhecida"

for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, header=None)

    current_entidade = None
    current_block = []

    for i, row in df.iterrows():
        entidade_raw = row[0]
        if pd.isna(entidade_raw):
            continue

        entidade = limpar_nome_entidade(entidade_raw)

        # Nova entidade encontrada
        if entidade != current_entidade:
            # Guardar bloco anterior
            if current_entidade and current_block:
                header = current_block[0]
                data_rows = current_block[1:]
                if current_entidade not in entidades_dict:
                    entidades_dict[current_entidade] = {"header": header, "data": []}
                entidades_dict[current_entidade]["data"].extend(data_rows)
            # Iniciar novo bloco
            current_entidade = entidade
            filtered_row = row.drop(labels=[1, 2, 3]).tolist()
            filtered_row[0] = limpar_nome_entidade(filtered_row[0])  # Limpar coluna A
            current_block = [filtered_row]
        else:
            filtered_row = row.drop(labels=[1, 2, 3]).tolist()
            filtered_row[0] = limpar_nome_entidade(filtered_row[0])  # Limpar coluna A
            current_block.append(filtered_row)

    # Guardar último bloco
    if current_entidade and current_block:
        header = current_block[0]
        data_rows = current_block[1:]
        if current_entidade not in entidades_dict:
            entidades_dict[current_entidade] = {"header": header, "data": []}
        entidades_dict[current_entidade]["data"].extend(data_rows)

# Criar ficheiro Excel com uma sheet por entidade
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    sheets_criadas = 0
    for entidade, content in entidades_dict.items():
        header = content["header"]
        data = content["data"]

        if not data or not any(pd.notna(cell) for row in data for cell in row):
            continue  # Ignorar se não houver dados válidos

        df_entidade = pd.DataFrame(data, columns=header)

        # Limpar nome da sheet (máx 31 caracteres, sem caracteres inválidos)
        sheet_name = re.sub(r'[\\/*?:[\]]', '_', entidade)[:31]
        if not sheet_name:
            sheet_name = "Entidade_Desconhecida"

        # Escrever sheet
        df_entidade.to_excel(writer, sheet_name=sheet_name, index=False)
        sheets_criadas += 1

if sheets_criadas == 0:
    raise ValueError("Nenhuma sheet válida foi criada. Verifica os dados de origem.")

print(f"Ficheiro gerado com {sheets_criadas} sheets por entidade: {output_file}")
