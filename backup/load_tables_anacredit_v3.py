import pandas as pd
import os
import unicodedata
import re
from sqlalchemy import create_engine

# Configuração da ligação à base de dados PostgreSQL
db_user = "postgres"
db_password = "admin"
db_host = "localhost"
db_port = "5432"
db_name = "anacredit_v2"
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Diretório onde estão os ficheiros Excel gerados
input_dir = "casos"

# Ordem de carregamento das tabelas com base nas dependências
ordem_carregamento = [
    "counterparty_reference",
    "instrument",
    "protection_received",
    "counterparty_risk",
    "counterparty_default",
    "financial",
    "accounting",
    "counterparty_instrument",
    "joint_liabilities",
    "instrument_protection_received"
]

# Mapeamento entre entidades (sheet) e tabelas SQL
entidade_para_tabela = {
    "instrument": "instrument",
    "financial": "financial",
    "accounting": "accounting",
    "counterparty_reference": "counterparty_reference",
    "counterparty_instrument": "counterparty_instrument",
    "instrument_protection_received": "instrument_protection_received",
    "protection_received": "protection_received",
    "counterparty_default": "counterparty_default",
    "counterparty_risk": "counterparty_risk",
    "joint_liabilities": "joint_liabilities"
}

# Mapeamento de atributos por tabela (normalizados)
atributos_por_tabela = {
    "instrument": [
        "contract_identifier", "instrument_identifier", "type_of_instrument", "amortisation_type", "currency",
        "fiduciary_instrument", "inception_date", "end_date_of_interest_only_period", "interest_rate_cap",
        "interest_rate_floor", "interest_rate_reset_frequency", "interest_rate_spread_margin", "interest_rate_type",
        "legal_final_maturity_date", "commitment_amount_at_inception", "payment_frequency", "project_finance_loan",
        "purpose", "recourse", "reference_rate", "settlement_date", "subordinated_debt",
        "syndicated_contract_identifier", "repayment_rights", "fair_value_credit_risk_change"
    ],
    "financial": [
        "contract_identifier", "instrument_identifier", "interest_rate", "next_interest_rate_reset_date",
        "default_status", "date_of_default_status", "transferred_amount", "arrears", "date_of_past_due",
        "type_of_securitisation", "outstanding_nominal_amount", "accrued_interest", "off_balance_sheet_amount"
    ],
    "accounting": [
        "contract_identifier", "instrument_identifier", "accounting_classification", "balance_sheet_recognition",
        "accumulated_write_offs", "accumulated_impairment_amount", "type_of_impairment",
        "impairment_assessment_method", "sources_of_encumbrance", "fair_value_credit_risk_change",
        "performing_status", "date_of_performing_status", "provisions_off_balance_sheet",
        "forbearance_status", "date_of_forbearance_status", "cumulative_recoveries",
        "prudential_portfolio", "carrying_amount"
    ],
    "counterparty_instrument": [
        "contract_identifier", "instrument_identifier", "counterparty_identifier", "counterparty_role"
    ],
    "instrument_protection_received": [
        "contract_identifier", "instrument_identifier", "protection_identifier",
        "protection_allocated_value", "third_party_priority_claims"
    ],
    "protection_received": [
        "protection_identifier", "protection_provider_identifier", "type_of_protection", "protection_value",
        "type_of_protection_value", "protection_valuation_approach", "real_estate_collateral_location",
        "date_of_protection_value", "maturity_date", "original_protection_value", "date_of_original_protection_value"
    ],
    "counterparty_default": [
        "counterparty_identifier", "default_status", "date_of_default_status"
    ],
    "counterparty_risk": [
        "counterparty_identifier", "probability_of_default"
    ],
    "counterparty_reference": [
        "counterparty_identifier", "lei", "national_identifier", "head_office_identifier",
        "immediate_parent_identifier", "ultimate_parent_identifier", "name", "address_street", "address_city",
        "address_county", "address_postal_code", "address_country", "legal_form", "institutional_sector",
        "economic_activity", "legal_proceedings_status", "date_of_legal_proceedings", "enterprise_size",
        "date_of_enterprise_size", "number_of_employees", "balance_sheet_total", "annual_turnover",
        "accounting_standard"
    ],
    "joint_liabilities": [
        "contract_identifier", "instrument_identifier", "counterparty_identifier", "joint_liability_amount"
    ]
}

# Função para normalizar nomes de colunas
def normalizar_coluna(nome):
    nome = str(nome).strip().lower()
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8')
    nome = re.sub(r'[^a-z0-9_]+', '_', nome)
    nome = re.sub(r'_+', '_', nome)
    return nome.strip('_')

# Função para normalizar nomes de entidades/sheets
def normalizar_entidade(nome):
    nome = str(nome).strip().lower()
    nome = re.sub(r'\s*dataset\s*$', '', nome)  # remove sufixo "dataset"
    nome = nome.replace("-", "_").replace(" ", "_")
    return nome

# Iterar sobre os ficheiros Excel
for file_name in os.listdir(input_dir):
    if not file_name.endswith(".xlsx"):
        continue
    file_path = os.path.join(input_dir, file_name)
    xls = pd.ExcelFile(file_path)

    for entidade in ordem_carregamento:
        if entidade not in [normalizar_entidade(s) for s in xls.sheet_names]:
            continue

        sheet_name = next((s for s in xls.sheet_names if normalizar_entidade(s) == entidade), None)
        if not sheet_name:
            continue

        tabela = entidade_para_tabela.get(entidade)
        atributos_validos = atributos_por_tabela.get(tabela)
        if not tabela or not atributos_validos:
            print(f"⚠️ Sheet ignorada (sem mapeamento): {sheet_name} → {entidade}")
            continue

        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if df.empty:
            print(f"⚠️ Sheet vazia: {sheet_name} em {file_name}")
            continue

        df.columns = [normalizar_coluna(col) for col in df.columns]
        df.replace("Non-applicable", pd.NA, inplace=True)
        df.replace("Non-applicable ", pd.NA, inplace=True)
        df.replace("Not required", pd.NA, inplace=True)
        df = df[[col for col in df.columns if col in atributos_validos]]

        try:
            df.to_sql(tabela, engine, if_exists='append', index=False)
            print(f"✅ Dados inseridos na tabela '{tabela}' a partir da sheet '{sheet_name}' do ficheiro '{file_name}'")
        except Exception as e:
            print(f"❌ Erro ao inserir '{sheet_name}' de '{file_name}' na tabela '{tabela}': {e}")