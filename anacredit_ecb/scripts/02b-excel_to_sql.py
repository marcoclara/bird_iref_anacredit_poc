################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import pandas as pd
import os
import unicodedata
import re
import numpy as np
from sqlalchemy import create_engine
import configparser

# Load database configuration from properties file
config = configparser.ConfigParser()
config.read('anacredit_ecb/database/db_config.properties')

db_host = config.get('database', 'host')
db_port = config.get('database', 'port')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_name = config.get('database', 'new_db_name')

# Connect to PostgreSQL database
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Folder with CSV file(s) to process
#input_dir = "anacredit_ecb/output"
input_dir = "anacredit_ecb/test"

# Mapping between original spreadsheet names and normalized table names
entidade_para_tabela = {
    "instrument": "instrument",
    "financial": "financial",
    "accounting": "accounting",
    "counterparty reference": "counterparty_reference",
    "counterparty-instrument": "counterparty_instrument",
    "instrument-protection received": "instrument_protection_received",
    "protection received": "protection_received",
    "counterparty default": "counterparty_default",
    "counterparty risk": "counterparty_risk",
    "joint liabilities": "joint_liabilities"
}

# Mapping of normalized table attributes
atributos_por_tabela = {
    "instrument": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "type_of_instrument", "amortisation_type", "currency",
        "fiduciary_instrument", "inception_date", "end_date_of_interestonly_period", "interest_rate_cap",
        "interest_rate_floor", "interest_rate_reset_frequency", "interest_rate_spreadmargin", "interest_rate_type",
        "legal_final_maturity_date", "commitment_amount_at_inception", "payment_frequency", "project_finance_loan",
        "purpose", "recourse", "reference_rate", "settlement_date", "subordinated_debt",
        "syndicated_contract_identifier", "repayment_rights", "fair_value_changes_before_purchase"
    ],
    "financial": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "interest_rate", "next_interest_rate_reset_date",
        "default_status_of_the_instrument", "date_of_the_default_status_of_the_instrument", "transferred_amount",
        "arrears_for_the_instrument", "date_of_past_due_for_the_instrument", "type_of_securitisation",
        "outstanding_nominal_amount", "accrued_interest", "offbalancesheet_amount"
    ],
    "accounting": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "accounting_classification_of_instruments",
        "balance_sheet_recognition", "accumulated_writeoffs", "accumulated_impairment_amount",
        "type_of_impairment", "impairment_assessment_method", "sources_of_encumbrance",
        "accumulated_changes_in_fair_value_due_to_credit_risk", "performing_status_of_the_instrument",
        "date_of_the_performing_status_of_the_instrument", "provisions_associated_with_offbalancesheet_exposures",
        "status_of_forbearance_and_renegotiation", "date_of_the_status_of_forbearance_and_renegotiation",
        "cumulative_recoveries_since_default", "prudential_portfolio", "carrying_amount"
    ],
    "counterparty_instrument": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "counterparty_identifier", "counterparty_role"
    ],
    "joint_liabilities": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "counterparty_identifier", "joint_liability_amount"
    ],
    "instrument_protection_received": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "contract_identifier", "instrument_identifier", "protection_identifier", "protection_allocated_value",
        "thirdparty_priority_claims_against_the_protection"
    ],
    "protection_received": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "protection_identifier", "protection_provider_identifier", "type_of_protection", "protection_value_",
        "type_of_protection_value", "protection_valuation_approach", "real_estate_collateral_location",
        "date_of_protection_value", "maturity_date_of_the_protection", "original_protection_value",
        "date_of_original_protection_value"
    ],
    "counterparty_default": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "counterparty_identifier", "default_status_of_the_counterparty", "date_of_the_default_status_of_the_counterparty"
    ],
    "counterparty_risk": [
        "reporting_reference_date", "reporting_agent_identifier", "observed_agent_identifier",
        "counterparty_identifier", "probability_of_default"
    ],
    "counterparty_reference": [
        "reporting_reference_date", "reporting_agent_identifier", "counterparty_identifier", "lei",
        "national_identifier", "head_office_undertaking_identifier", "immediate_parent_undertaking_identifier",
        "ultimate_parent_undertaking_identifier", "name", "address_street", "address_citytownvillage",
        "address_countyadministrative_division", "address_postal_code", "address_country", "legal_form",
        "institutional_sector", "economic_activity", "status_of_legal_proceedings", "date_of_initiation_of_legal_proceedings",
        "enterprise_size", "date_of_enterprise_size", "number_of_employees", "balance_sheet_total",
        "annual_turnover", "accounting_standard"
    ]
}

# Column name normalization function
def normalizar_coluna(nome):
    nome = str(nome).replace('/', '')  # remove slashes
    nome = str(nome).strip().lower()   # lower case
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8') # encoding
    nome = re.sub(r'[^a-z0-9_]+', '_', nome)
    nome = re.sub(r'_+', '_', nome)
    return nome.strip('_')

# Excel file iteration
for file_name in os.listdir(input_dir):
    if not file_name.endswith(".xlsx"):
        continue
    file_path = os.path.join(input_dir, file_name)
    xls = pd.ExcelFile(file_path, engine="openpyxl")
    for entidade_original, tabela in entidade_para_tabela.items():
        sheet_name = next((s for s in xls.sheet_names if s.strip().lower() == entidade_original.strip().lower()), None)
        if not sheet_name:
            continue
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        if df.empty:
            print(f"⚠️ Empty sheet: {sheet_name} em {file_name}")
            continue
        df.columns = [normalizar_coluna(col) for col in df.columns]
        df = df.dropna(axis=1, how='all')
        #df.replace(["Non-applicable", "Not required"], pd.NA, inplace=True)
        #df.replace(["Non-applicable", "Not required"], None, inplace=True)
        df.replace(["Non-applicable", "Not required"], np.nan, inplace=True)
        colunas_validas = atributos_por_tabela.get(tabela, [])
        df = df[[col for col in df.columns if col in colunas_validas]]
        
        # Cleanup white spaces in text values
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()

        try:
            df.to_sql(tabela, engine, if_exists='append', index=False)
            print(f"✅ Data inserted for table '{tabela}' from sheet '{sheet_name}' of file '{file_name}'")
        except Exception as e:
            print(f"❌ Error while inserting '{sheet_name}' from '{file_name}' into table '{tabela}': {e}")
