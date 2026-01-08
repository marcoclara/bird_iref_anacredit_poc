import pandas as pd
import re

# Ficheiro de entrada e saída
input_file = "ecb_dataset/AnaCredit_Entidades_Separadas.xlsx"
output_file = "ecb_dataset/AnaCredit_Entidades_Sem_Duplicados.xlsx"

# Carregar todas as sheets
xls = pd.ExcelFile(input_file)
sheet_names = xls.sheet_names

# Função para limpar nome da sheet
def limpar_nome(nome):
    return re.sub(r'[\\/*?:[\]]', '_', nome).strip()[:31]

# Criar novo ficheiro Excel
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet in sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)

        if df.empty or len(df.columns) < 2:
            continue  # Ignorar sheets sem dados

        # Remover duplicados
        df_sem_duplicados = df.drop_duplicates()

        # Escrever no novo ficheiro
        df_sem_duplicados.to_excel(writer, sheet_name=limpar_nome(sheet), index=False)

print(f"✅ Ficheiro gerado sem duplicados: {output_file}")