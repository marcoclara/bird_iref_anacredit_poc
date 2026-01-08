import pandas as pd
import openpyxl

# Caminho para o ficheiro original
input_file = "ecb_dataset/AnaCredit_Manual_Part_III_Examples_of_complete_reports.xlsx"
output_file = "ecb_dataset/AnaCredit_Agregado_por_Entidade.xlsx"

# Carregar todas as sheets
xls = pd.ExcelFile(input_file)
sheet_names = [s for s in xls.sheet_names if s.startswith("CASE")]

# Dicionário para armazenar dados por entidade
entidades_dict = {}

for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, header=None)

    current_entidade = None
    current_block = []

    for i, row in df.iterrows():
        entidade = row[0]
        if pd.isna(entidade):
            continue

        # Nova entidade encontrada
        if entidade != current_entidade:
            # Guardar bloco anterior
            if current_entidade and current_block:
                if current_entidade not in entidades_dict:
                    entidades_dict[current_entidade] = []
                entidades_dict[current_entidade].extend(current_block)
            # Iniciar novo bloco
            current_entidade = entidade
            current_block = [row.drop(labels=[1]).tolist()]  # Ignorar coluna B
        else:
            current_block.append(row.drop(labels=[1]).tolist())

    # Guardar último bloco
    if current_entidade and current_block:
        if current_entidade not in entidades_dict:
            entidades_dict[current_entidade] = []
        entidades_dict[current_entidade].extend(current_block)

# Criar DataFrame final
final_rows = []
for entidade in sorted(entidades_dict.keys()):
    final_rows.append([f"Entidade: {entidade}"] + [""] * (len(entidades_dict[entidade][0]) - 1))
    final_rows.extend(entidades_dict[entidade])
    final_rows.append([""] * len(entidades_dict[entidade][0]))  # Linha em branco entre blocos
final_df = pd.DataFrame(final_rows)

# Guardar em novo ficheiro Excel
final_df.to_excel(output_file, index=False, header=False)

print(f"Ficheiro agregado guardado como: {output_file}")