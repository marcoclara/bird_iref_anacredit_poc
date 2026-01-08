import os
import pandas as pd
from openpyxl import load_workbook

# Caminho onde estão os ficheiros case
caminho_ficheiros = "casos_separados"

# Iterar por todos os ficheiros .xlsx na pasta
for nome_ficheiro in os.listdir(caminho_ficheiros):
    if nome_ficheiro.endswith(".xlsx"):
        caminho_completo = os.path.join(caminho_ficheiros, nome_ficheiro)
        excel = pd.ExcelFile(caminho_completo)
        
        # Dicionário para guardar folhas limpas
        folhas_limpas = {}

        for nome_folha in excel.sheet_names:
            df = excel.parse(nome_folha)
            df_sem_duplicados = df.drop_duplicates()
            folhas_limpas[nome_folha] = df_sem_duplicados

        # Guardar num novo ficheiro (ou sobrescrever)
        with pd.ExcelWriter(caminho_completo, engine='openpyxl', mode='w') as writer:
            for nome_folha, df in folhas_limpas.items():
                df.to_excel(writer, sheet_name=nome_folha, index=False)

print("Remoção de duplicados concluída para todos os ficheiros.")