import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Configuração da base de dados PostgreSQL
db_config = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'anacredit_v2',
    'user': 'postgres',
    'password': 'admin'
}

# Caminho para o ficheiro Excel tratado
#excel_file = "ecb_dataset/AnaCredit_Entidades_Separadas.xlsx"
#excel_file = "ecb_dataset/AnaCredit_Entidades_Sem_Duplicados.xlsx"
excel_file = "casos/CASE 1.xlsx"

sheet_to_table = {
    "Instrument": {
        "table": "instrument",
        "columns": [
            "contract_identifier", "instrument_identifier", "type_of_instrument", "amortisation_type",
            "currency", "fiduciary_instrument", "inception_date", "end_date_of_interest_only_period",
            "interest_rate_cap", "interest_rate_floor", "interest_rate_reset_frequency",
            "interest_rate_spread_margin", "interest_rate_type", "legal_final_maturity_date",
            "commitment_amount_at_inception", "payment_frequency", "project_finance_loan", "purpose",
            "recourse", "reference_rate", "settlement_date", "subordinated_debt",
            "syndicated_contract_identifier", "repayment_rights", "fair_value_changes_due_to_credit_risk"
        ]
    },
    "Financial": {
        "table": "financial",
        "columns": [
            "contract_identifier", "instrument_identifier", "interest_rate", "next_interest_rate_reset_date",
            "default_status", "date_of_default_status", "transferred_amount", "arrears",
            "date_of_past_due", "type_of_securitisation", "outstanding_nominal_amount",
            "accrued_interest", "off_balance_sheet_amount"
        ]
    },
    "Accounting": {
        "table": "accounting",
        "columns": [
            "contract_identifier", "instrument_identifier", "accounting_classification",
            "balance_sheet_recognition", "accumulated_write_offs", "accumulated_impairment_amount",
            "type_of_impairment", "impairment_assessment_method", "sources_of_encumbrance",
            "fair_value_changes_due_to_credit_risk", "performing_status", "date_of_performing_status",
            "provisions_off_balance_sheet", "forbearance_status", "date_of_forbearance_status",
            "cumulative_recoveries", "prudential_portfolio", "carrying_amount"
        ]
    },
    "Counterparty-instrument": {
        "table": "counterparty_instrument",
        "columns": [
            "contract_identifier", "instrument_identifier", "counterparty_identifier", "counterparty_role"
        ]
    },
    "Joint liabilities": {
        "table": "joint_liabilities",
        "columns": [
            "contract_identifier", "instrument_identifier", "counterparty_identifier", "joint_liability_amount"
        ]
    },
    "Instrument-protection received": {
        "table": "instrument_protection_received",
        "columns": [
            "contract_identifier", "instrument_identifier", "protection_identifier",
            "protection_allocated_value", "third_party_priority_claims"
        ]
    },
    "Protection received": {
        "table": "protection_received",
        "columns": [
            "protection_identifier", "protection_provider_identifier", "type_of_protection",
            "protection_value", "type_of_protection_value", "protection_valuation_approach",
            "real_estate_collateral_location", "date_of_protection_value", "maturity_date",
            "original_protection_value", "date_of_original_protection_value"
        ]
    },
    "Counterparty default": {
        "table": "counterparty_default",
        "columns": [
            "counterparty_identifier", "default_status", "date_of_default_status"
        ]
    },
    "Counterparty risk": {
        "table": "counterparty_risk",
        "columns": [
            "counterparty_identifier", "probability_of_default"
        ]
    },
    "Counterparty reference": {
        "table": "counterparty_reference",
        "columns": [
            "counterparty_identifier", "lei", "national_identifier", "head_office_identifier",
            "immediate_parent_identifier", "ultimate_parent_identifier", "name", "address_street",
            "address_city", "address_county", "address_postal_code", "address_country", "legal_form",
            "institutional_sector", "economic_activity", "legal_proceedings_status",
            "date_of_legal_proceedings", "enterprise_size", "date_of_enterprise_size",
            "number_of_employees", "balance_sheet_total", "annual_turnover", "accounting_standard"
        ]
    }
}

def carregar_dados_para_postgres():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    xls = pd.ExcelFile(excel_file)
    for sheet_name in xls.sheet_names:
        if sheet_name not in sheet_to_table:
            print(f"Sheet ignorada: {sheet_name}")
            continue

        tabela_info = sheet_to_table[sheet_name]
        tabela = tabela_info["table"]
        colunas_sql = tabela_info["columns"]

        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Tentar alinhar colunas do Excel com as esperadas na tabela
        colunas_excel = df.columns.str.lower().str.replace(" ", "_").str.strip()
        df.columns = colunas_excel

        # Filtrar apenas colunas que existem na tabela SQL
        df_filtrado = df[[col for col in colunas_sql if col in df.columns]]

        # Substituir 'Non-applicable' e NaN por None
        df_filtrado = df_filtrado.replace("Non-applicable", None)
        df_filtrado = df_filtrado.replace("Non-applicable ", None)
        df_filtrado = df_filtrado.where(pd.notnull(df_filtrado), None)

        valores = [tuple(row) for row in df_filtrado.to_numpy()]
        colunas_insert = ', '.join(df_filtrado.columns)

        sql = f"INSERT INTO {tabela} ({colunas_insert}) VALUES %s"

        try:
            execute_values(cursor, sql, valores)
            conn.commit()
            print(f"✅ Dados inseridos na tabela: {tabela}")
        except Exception as e:
            conn.rollback()
            print(f"❌ Erro ao inserir na tabela {tabela}: {e}")

    cursor.close()
    conn.close()

# Executar
carregar_dados_para_postgres()