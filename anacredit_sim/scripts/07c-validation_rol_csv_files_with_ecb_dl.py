################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import pandas as pd
import os
import requests
import xml.etree.ElementTree as ET

# Directory containing your CSV files
DATA_DIR = "anacredit_sim/output/csv/rol"  # Adjust if needed

# -------------------------------
# Fetch and Parse NACE Codes from XML
# -------------------------------

def fetch_nace_codes_from_xml():
    url = "https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/nace2/20241120-0/xml/xml/SDMX_NACE_REV2.xml&fileName=SDMX_NACE_REV2.xml"
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Extract codes from SDMX structure
        # Look for elements like <Code id="A"> or similar
        namespace = {'structure': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'}
        codes = []
        for code in root.findall(".//structure:Code", namespace):
            code_id = code.attrib.get('id')
            if code_id and len(code_id) == 1 and code_id.isalpha():
                codes.append(code_id)
        return sorted(set(codes))
    except Exception as e:
        print(f"⚠️ Failed to fetch or parse NACE codes: {e}")
        return []

# -------------------------------
# Hardcoded ECB Code Lists
# -------------------------------

VALID_SECTOR_CODES = ['NFC', 'HH', 'GOV', 'INS', 'PF', 'MF', 'CB', 'IF', 'OTH']
VALID_CURRENCY_CODES = ['EUR', 'USD', 'GBP', 'CHF', 'JPY']
VALID_CONTRACT_STATUS = ['active', 'terminated', 'defaulted']
VALID_INSTRUMENT_TYPES = ['Loan', 'Overdraft', 'Credit Line']
VALID_PROTECTION_TYPES = ['Mortgage', 'Pledge', 'Personal Guarantee']
VALID_RATE_TYPES = ['Fixed', 'Variable']
VALID_REFERENCE_RATES = ['EURIBOR', 'LIBOR', 'SOFR']
VALID_RESIDENCY_COUNTRIES = ['PT', 'ES', 'FR', 'DE', 'IT']

# -------------------------------
# Validation Helpers
# -------------------------------

def validate_column(df, column, valid_values, file_name):
    if not df[column].isin(valid_values).all():
        print(f"[{file_name}] ❌ Invalid values in column '{column}'")
    else:
        print(f"[{file_name}] ✅ Column '{column}' passed code list validation.")

# -------------------------------
# Validation Functions
# -------------------------------

def validate_counterparty():
    file = os.path.join(DATA_DIR, "ROL_Counterparty_v2.csv")
    df = pd.read_csv(file)
    assert df['counterpartyidentifier'].is_unique, "Duplicate CounterpartyIdentifier"
    assert df['lei'].notnull().all(), "Missing LEI"
    validate_column(df, 'sectorcode', VALID_SECTOR_CODES, "ROL_Counterparty")
    validate_column(df, 'residencycountry', VALID_RESIDENCY_COUNTRIES, "ROL_Counterparty")
    nace_codes = fetch_nace_codes_from_xml()
    validate_column(df, 'nacecode', nace_codes, "ROL_Counterparty")
    print("[ROL_Counterparty] ✅ Validation complete.\n")

def validate_instrument():
    file = os.path.join(DATA_DIR, "ROL_Instrument.csv")
    df = pd.read_csv(file)
    assert df['instrumentidentifier'].is_unique, "Duplicate InstrumentIdentifier"
    validate_column(df, 'instrumenttype', VALID_INSTRUMENT_TYPES, "ROL_Instrument")
    validate_column(df, 'currency', VALID_CURRENCY_CODES, "ROL_Instrument")
    assert pd.to_datetime(df['maturitydate'], errors='coerce').notnull().all(), "Invalid MaturityDate format"
    assert (df['remainingmaturity'] > 0).all(), "RemainingMaturity must be positive"
    print("[ROL_Instrument] ✅ Validation complete.\n")

def validate_contract():
    file = os.path.join(DATA_DIR, "ROL_Contract.csv")
    df = pd.read_csv(file)
    assert df['contractidentifier'].is_unique, "Duplicate ContractIdentifier"
    validate_column(df, 'contractstatus', VALID_CONTRACT_STATUS, "ROL_Contract")
    assert pd.to_datetime(df['contractdate'], errors='coerce').notnull().all(), "Invalid ContractDate format"
    print("[ROL_Contract] ✅ Validation complete.\n")

def validate_protection():
    file = os.path.join(DATA_DIR, "ROL_Protection.csv")
    df = pd.read_csv(file)
    assert df['protectionidentifier'].is_unique, "Duplicate ProtectionIdentifier"
    validate_column(df, 'protectiontype', VALID_PROTECTION_TYPES, "ROL_Protection")
    assert (df['protectionamount'] > 0).all(), "ProtectionAmount must be positive"
    print("[ROL_Protection] ✅ Validation complete.\n")

def validate_interest_rate_terms():
    file = os.path.join(DATA_DIR, "ROL_InterestRateTerms.csv")
    df = pd.read_csv(file)
    assert df['ratetermidentifier'].is_unique, "Duplicate RateTermIdentifier"
    validate_column(df, 'ratetype', VALID_RATE_TYPES, "ROL_InterestRateTerms")
    validate_column(df, 'referencerate', VALID_REFERENCE_RATES, "ROL_InterestRateTerms")
    assert (df['spread'] >= 0).all(), "Spread must be non-negative"
    print("[ROL_InterestRateTerms] ✅ Validation complete.\n")

def validate_accounting():
    file = os.path.join(DATA_DIR, "ROL_Accounting.csv")
    df = pd.read_csv(file)
    assert df['accountingidentifier'].is_unique, "Duplicate AccountingIdentifier"
    assert (df['amountoutstanding'] >= df['amountinarrears']).all(), "Outstanding < Arrears"
    assert (df[['amountoutstanding', 'amountinarrears', 'provisionamount', 'writeoffamount']] >= 0).all().all(), "Negative values found"
    print("[ROL_Accounting] ✅ Validation complete.\n")

# -------------------------------
# Run All Validations
# -------------------------------

validate_counterparty()
validate_instrument()
validate_contract()
validate_protection()
validate_interest_rate_terms()
