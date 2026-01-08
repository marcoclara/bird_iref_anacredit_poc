-- =============================================================================
-- BIRD & IReF
-- Data Model Definition & Implementation for BIRD and IReF Framework Enablement
-- Universidade Aberta - MEIW - Marco Clara (nº 2302597)
-- =============================================================================

-- =============================================================================
-- INSTRUMENT TABLE
-- credit agreement or loan contract reported by a credit institution
-- =============================================================================
DROP TABLE IF EXISTS instrument CASCADE;
CREATE TABLE instrument (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    type_of_instrument TEXT,
    amortisation_type TEXT,
    currency TEXT,
    fiduciary_instrument TEXT,
    inception_date DATE,
    end_date_of_interestonly_period DATE,
    interest_rate_cap TEXT,
    interest_rate_floor TEXT,
    interest_rate_reset_frequency TEXT,
    interest_rate_spreadmargin TEXT,
    interest_rate_type TEXT,
    legal_final_maturity_date DATE,
    commitment_amount_at_inception INTEGER,
    payment_frequency TEXT,
    project_finance_loan TEXT,
    purpose TEXT,
    recourse TEXT,
    reference_rate TEXT,
    settlement_date DATE,
    subordinated_debt TEXT,
    syndicated_contract_identifier TEXT,
    repayment_rights TEXT,
    fair_value_changes_before_purchase TEXT,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier)
);

-- =============================================================================
-- FINANCIAL TABLE
-- financial characteristics of each reported credit instrument
-- =============================================================================
DROP TABLE IF EXISTS financial CASCADE;
CREATE TABLE financial (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    interest_rate FLOAT,
    next_interest_rate_reset_date DATE,
    default_status_of_the_instrument TEXT,
    date_of_the_default_status_of_the_instrument DATE,
    transferred_amount INTEGER,
    arrears_for_the_instrument INTEGER,
    date_of_past_due_for_the_instrument DATE,
    type_of_securitisation TEXT,
    outstanding_nominal_amount INTEGER,
    accrued_interest FLOAT,
    offbalancesheet_amount TEXT,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier)
);

-- =============================================================================
-- ACCOUNTING TABLE
-- accounting related attributes of credit instruments
-- =============================================================================
DROP TABLE IF EXISTS accounting CASCADE;
CREATE TABLE accounting (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    accounting_classification_of_instruments TEXT,
    balance_sheet_recognition TEXT,
    accumulated_writeoffs INTEGER,
    accumulated_impairment_amount INTEGER,
    type_of_impairment TEXT,
    impairment_assessment_method TEXT,
    sources_of_encumbrance TEXT,
    accumulated_changes_in_fair_value_due_to_credit_risk TEXT,
    performing_status_of_the_instrument TEXT,
    date_of_the_performing_status_of_the_instrument DATE,
    provisions_associated_with_offbalancesheet_exposures TEXT,
    status_of_forbearance_and_renegotiation TEXT,
    date_of_the_status_of_forbearance_and_renegotiation DATE,
    cumulative_recoveries_since_default TEXT,
    prudential_portfolio TEXT,
    carrying_amount TEXT,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier)
);

-- =============================================================================
-- COUNTERPARTY INSTRUMENT TABLE
-- relational link between credit instruments and associated counterparties
-- =============================================================================
DROP TABLE IF EXISTS counterparty_instrument CASCADE;
CREATE TABLE counterparty_instrument (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    counterparty_identifier TEXT,
    counterparty_role TEXT,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier, counterparty_role)
);

-- =============================================================================
-- INSTRUMENT PROTECTION TABLE
-- information on protection items such as collateral, guarantees, and credit derivatives
-- =============================================================================
DROP TABLE IF EXISTS instrument_protection_received CASCADE;
CREATE TABLE instrument_protection_received (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    protection_identifier TEXT,
    protection_allocated_value INTEGER,
    thirdparty_priority_claims_against_the_protection INTEGER,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier, protection_identifier)
);

-- =============================================================================
-- PROTECTION RECEIVED TABLE
-- information on individual protection items such as collateral, guarantees, and credit derivatives
-- =============================================================================
DROP TABLE IF EXISTS protection_received CASCADE;
CREATE TABLE protection_received (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    protection_identifier TEXT,
    protection_provider_identifier TEXT,
    type_of_protection TEXT,
    protection_value_ INTEGER,
    type_of_protection_value TEXT,
    protection_valuation_approach TEXT,
    real_estate_collateral_location TEXT,
    date_of_protection_value DATE,
    maturity_date_of_the_protection DATE,
    original_protection_value INTEGER,
    date_of_original_protection_value DATE,
	PRIMARY KEY (reporting_reference_date, protection_identifier, protection_provider_identifier)
);

-- =============================================================================
-- COUNTERPARTY DEFAULT TABLE
-- status of a counterparty, indicating whether the legal entity is considered to be in default
-- =============================================================================
DROP TABLE IF EXISTS counterparty_default CASCADE;
CREATE TABLE counterparty_default (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    counterparty_identifier TEXT,
    default_status_of_the_counterparty TEXT,
    date_of_the_default_status_of_the_counterparty DATE,
	PRIMARY KEY (reporting_reference_date, counterparty_identifier)
);

-- =============================================================================
-- COUNTERPARTY RISK TABLE
-- risk related attributes of counterparties involved in credit instruments or providing protection
-- =============================================================================
DROP TABLE IF EXISTS counterparty_risk CASCADE;
CREATE TABLE counterparty_risk (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    counterparty_identifier TEXT,
    probability_of_default FLOAT,
	PRIMARY KEY (reporting_reference_date, counterparty_identifier)
);

-- =============================================================================
-- COUNTERPARTY REFERENCE TABLE
-- static identification and classification data about legal entities involved in credit relationships
-- =============================================================================
DROP TABLE IF EXISTS counterparty_reference CASCADE;
CREATE TABLE counterparty_reference (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    counterparty_identifier TEXT,
    lei TEXT,
    national_identifier TEXT,
    head_office_undertaking_identifier TEXT,
    immediate_parent_undertaking_identifier TEXT,
    ultimate_parent_undertaking_identifier TEXT,
    name TEXT,
    address_street TEXT,
    address_citytownvillage TEXT,
    address_countyadministrative_division TEXT,
    address_postal_code TEXT,
    address_country TEXT,
    legal_form TEXT,
    institutional_sector TEXT,
    economic_activity FLOAT,
    status_of_legal_proceedings TEXT,
    date_of_initiation_of_legal_proceedings DATE,
    enterprise_size TEXT,
    date_of_enterprise_size DATE,
    number_of_employees TEXT,
    balance_sheet_total TEXT,
    annual_turnover TEXT,
    accounting_standard TEXT,
	PRIMARY KEY (reporting_reference_date, counterparty_identifier)
);

-- =============================================================================
-- JOINT LIABILITIES TABLE
-- credit instruments where multiple debtors share liability
-- =============================================================================
DROP TABLE IF EXISTS joint_liabilities CASCADE;
CREATE TABLE joint_liabilities (
    reporting_reference_date DATE,
    reporting_agent_identifier TEXT,
    observed_agent_identifier TEXT,
    contract_identifier TEXT,
    instrument_identifier TEXT,
    counterparty_identifier INTEGER,
    joint_liability_amount INTEGER,
	PRIMARY KEY (reporting_reference_date, contract_identifier, instrument_identifier, counterparty_identifier)
);
