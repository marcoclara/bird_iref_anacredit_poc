import pandas as pd
import re
import os

# Caminho para o ficheiro original
input_file = "anacredit_v2/input_dataset/AnaCredit_Manual_Part_III_Examples_of_complete_reports.xlsx"
output_dir = "anacredit_v2/output_dataset"
os.makedirs(output_dir, exist_ok=True)

# Carregar todas as sheets que começam por "CASE"
xls = pd.ExcelFile(input_file)
sheet_names = [s for s in xls.sheet_names if s.startswith("CASE")]

# Atributos a omitir nas tabelas finais
atributos_a_omitir = {
    "Reporting agent identifier",
    "Observed agent identifier"
}

def limpar_nome_entidade(nome):
    nome_limpo = re.sub(r'\s*dataset\s*$', '', str(nome), flags=re.IGNORECASE).strip()
    return nome_limpo if nome_limpo else "Entidade_Desconhecida"

for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, header=None)
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
                df_entidade = pd.DataFrame(data, columns=header)

                # Verifica se existe a coluna de data
                nome_coluna_data = "Reporting reference date"
                if nome_coluna_data in df_entidade.columns:
                    try:
                        df_entidade[nome_coluna_data] = pd.to_datetime(
                            df_entidade[nome_coluna_data].astype(str).str.strip(),
                            format="%Y-%m-%d",
                            errors="coerce"
                        )
                        data_mais_recente = df_entidade[nome_coluna_data].max()
                        df_entidade = df_entidade[df_entidade[nome_coluna_data] == data_mais_recente]
                    except Exception as e:
                        print(f"⚠️ Erro ao converter datas para entidade {entidade}: {e}")
                else:
                    print(f"⚠️ Coluna '{nome_coluna_data}' não encontrada para entidade {entidade}. Nenhum filtro aplicado.")

                df_entidade = df_entidade.drop(columns=[col for col in df_entidade.columns if col in atributos_a_omitir], errors='ignore')

                sheet_name = re.sub(r'[\\/*?:[\]]', '_', entidade)[:31]
                if not sheet_name:
                    sheet_name = "Entidade_Desconhecida"
                df_entidade.to_excel(writer, sheet_name=sheet_name, index=False)
                sheets_criadas += 1

    print(f"✅ Ficheiro gerado: {output_file} com {sheets_criadas} entidades.")