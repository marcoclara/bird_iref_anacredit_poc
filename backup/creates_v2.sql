-- Tabela: instrument
CREATE TABLE instrument (
    instrument_identifier TEXT PRIMARY KEY,
    contract_identifier TEXT NOT NULL,
    type_of_instrument TEXT,
    amortisation_type TEXT,
    currency TEXT,
    fiduciary_instrument TEXT,
    inception_date DATE,
    end_date_of_interest_only_period DATE,
    interest_rate_cap NUMERIC,
    interest_rate_floor NUMERIC,
    interest_rate_reset_frequency TEXT,
    interest_rate_spread_margin NUMERIC,
    interest_rate_type TEXT,
    legal_final_maturity_date DATE,
    commitment_amount_at_inception NUMERIC,
    payment_frequency TEXT,
    project_finance_loan TEXT,
    purpose TEXT,
    recourse TEXT,
    reference_rate TEXT,
    settlement_date DATE,
    subordinated_debt TEXT,
    syndicated_contract_identifier TEXT,
    repayment_rights TEXT,
    fair_value_changes_due_to_credit_risk NUMERIC
);

-- Tabela: financial
CREATE TABLE financial (
    instrument_identifier TEXT PRIMARY KEY,
    contract_identifier TEXT NOT NULL,
    interest_rate NUMERIC,
    next_interest_rate_reset_date DATE,
    default_status TEXT,
    date_of_default_status DATE,
    transferred_amount NUMERIC,
    arrears NUMERIC,
    date_of_past_due DATE,
    type_of_securitisation TEXT,
    outstanding_nominal_amount NUMERIC,
    accrued_interest NUMERIC,
    off_balance_sheet_amount NUMERIC,
    FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Tabela: accounting
CREATE TABLE accounting (
    instrument_identifier TEXT PRIMARY KEY,
    contract_identifier TEXT NOT NULL,
    accounting_classification TEXT,
    balance_sheet_recognition TEXT,
    accumulated_write_offs NUMERIC,
    accumulated_impairment_amount NUMERIC,
    type_of_impairment TEXT,
    impairment_assessment_method TEXT,
    sources_of_encumbrance TEXT,
    fair_value_changes_due_to_credit_risk NUMERIC,
    performing_status TEXT,
    date_of_performing_status DATE,
    provisions_off_balance_sheet NUMERIC,
    forbearance_status TEXT,
    date_of_forbearance_status DATE,
    cumulative_recoveries NUMERIC,
    prudential_portfolio TEXT,
    carrying_amount NUMERIC,
    FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Tabela: counterparty_reference
CREATE TABLE counterparty_reference (
    counterparty_identifier TEXT PRIMARY KEY,
    LEI TEXT,
    national_identifier TEXT,
    head_office_identifier TEXT,
    immediate_parent_identifier TEXT,
    ultimate_parent_identifier TEXT,
    name TEXT,
    address_street TEXT,
    address_city TEXT,
    address_county TEXT,
    address_postal_code TEXT,
    address_country TEXT,
    legal_form TEXT,
    institutional_sector TEXT,
    economic_activity TEXT,
    legal_proceedings_status TEXT,
    date_of_legal_proceedings DATE,
    enterprise_size TEXT,
    date_of_enterprise_size DATE,
    number_of_employees INTEGER,
    balance_sheet_total NUMERIC,
    annual_turnover NUMERIC,
    accounting_standard TEXT
);

-- Tabela: counterparty_instrument
DROP TABLE counterparty_instrument;
CREATE TABLE counterparty_instrument (
    contract_identifier TEXT,
    instrument_identifier TEXT,
    counterparty_identifier TEXT,
    counterparty_role TEXT,
    PRIMARY KEY (contract_identifier, instrument_identifier, counterparty_identifier, counterparty_role),
    FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier),
    FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_reference(counterparty_identifier)
);

-- Tabela: joint_liabilities
CREATE TABLE joint_liabilities (
    contract_identifier TEXT,
    instrument_identifier TEXT,
    counterparty_identifier TEXT,
    joint_liability_amount NUMERIC,
    PRIMARY KEY (contract_identifier, instrument_identifier, counterparty_identifier),
    FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier),
    FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_reference(counterparty_identifier)
);

-- Tabela: instrument_protection_received
CREATE TABLE instrument_protection_received (
    contract_identifier TEXT,
    instrument_identifier TEXT,
    protection_identifier TEXT,
    protection_allocated_value NUMERIC,
    third_party_priority_claims NUMERIC,
    PRIMARY KEY (contract_identifier, instrument_identifier, protection_identifier),
    FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Tabela: protection_received
CREATE TABLE protection_received (
    protection_identifier TEXT PRIMARY KEY,
    protection_provider_identifier TEXT,
    type_of_protection TEXT,
    protection_value NUMERIC,
    type_of_protection_value TEXT,
    protection_valuation_approach TEXT,
    real_estate_collateral_location TEXT,
    date_of_protection_value DATE,
    maturity_date DATE,
    original_protection_value NUMERIC,
    date_of_original_protection_value DATE
);

-- Tabela: counterparty_default
CREATE TABLE counterparty_default (
    counterparty_identifier TEXT PRIMARY KEY,
    default_status TEXT,
    date_of_default_status DATE,
    FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_reference(counterparty_identifier)
);

-- Tabela: counterparty_risk
CREATE TABLE counterparty_risk (
    counterparty_identifier TEXT PRIMARY KEY,
    probability_of_default NUMERIC,
    FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_reference(counterparty_identifier)
);
