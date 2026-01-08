-- Instrument
DROP TABLE IF EXISTS instrument CASCADE;
CREATE TABLE instrument (
 contract_identifier TEXT,
 instrument_identifier TEXT,
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
 fair_value_credit_risk_change NUMERIC
);

-- Financial
DROP TABLE IF EXISTS financial CASCADE;
CREATE TABLE financial (
 contract_identifier TEXT,
 instrument_identifier TEXT,
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
 FOREIGN KEY (contract_identifier) REFERENCES instrument(contract_identifier),
 FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Accounting
DROP TABLE IF EXISTS accounting CASCADE;
CREATE TABLE accounting (
 contract_identifier TEXT,
 instrument_identifier TEXT,
 accounting_classification TEXT,
 balance_sheet_recognition TEXT,
 accumulated_write_offs NUMERIC,
 accumulated_impairment_amount NUMERIC,
 type_of_impairment TEXT,
 impairment_assessment_method TEXT,
 sources_of_encumbrance TEXT,
 fair_value_credit_risk_change NUMERIC,
 performing_status TEXT,
 date_of_performing_status DATE,
 provisions_off_balance_sheet NUMERIC,
 forbearance_status TEXT,
 date_of_forbearance_status DATE,
 cumulative_recoveries NUMERIC,
 prudential_portfolio TEXT,
 carrying_amount NUMERIC,
 FOREIGN KEY (contract_identifier) REFERENCES instrument(contract_identifier),
 FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Counterparty Instrument
DROP TABLE IF EXISTS counterparty_instrument CASCADE;
CREATE TABLE counterparty_instrument (
 contract_identifier TEXT,
 instrument_identifier TEXT,
 counterparty_identifier TEXT,
 counterparty_role TEXT,
 PRIMARY KEY (contract_identifier, instrument_identifier, counterparty_identifier, counterparty_role),
 FOREIGN KEY (contract_identifier) REFERENCES instrument(contract_identifier),
 FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Joint Liabilities
DROP TABLE IF EXISTS joint_liabilities CASCADE;
CREATE TABLE joint_liabilities (
 contract_identifier TEXT,
 instrument_identifier TEXT,
 counterparty_identifier TEXT,
 joint_liability_amount NUMERIC,
 FOREIGN KEY (contract_identifier) REFERENCES instrument(contract_identifier),
 FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier),
 FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_instrument(counterparty_identifier)
);

-- Instrument Protection Received
DROP TABLE IF EXISTS instrument_protection_received CASCADE;
CREATE TABLE instrument_protection_received (
 contract_identifier TEXT,
 instrument_identifier TEXT,
 protection_identifier TEXT,
 protection_allocated_value NUMERIC,
 third_party_priority_claims NUMERIC,
 FOREIGN KEY (contract_identifier) REFERENCES instrument(contract_identifier),
 FOREIGN KEY (instrument_identifier) REFERENCES instrument(instrument_identifier)
);

-- Protection Received
DROP TABLE IF EXISTS protection_received CASCADE;
CREATE TABLE protection_received (
 protection_identifier TEXT,
 protection_provider_identifier TEXT,
 type_of_protection TEXT,
 protection_value NUMERIC,
 type_of_protection_value TEXT,
 protection_valuation_approach TEXT,
 real_estate_collateral_location TEXT,
 date_of_protection_value DATE,
 maturity_date DATE,
 original_protection_value NUMERIC,
 date_of_original_protection_value DATE,
 FOREIGN KEY (protection_identifier) REFERENCES instrument_protection_received(protection_identifier)
);



-- Counterparty Default
DROP TABLE IF EXISTS counterparty_default CASCADE;
CREATE TABLE counterparty_default (
 counterparty_identifier TEXT,
 default_status TEXT,
 date_of_default_status DATE,
 FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_instrument(counterparty_identifier)
);

-- Counterparty Risk
DROP TABLE IF EXISTS counterparty_risk CASCADE;
CREATE TABLE counterparty_risk (
 counterparty_identifier TEXT,
 probability_of_default NUMERIC,
 FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_instrument(counterparty_identifier)
);

-- Counterparty Reference
DROP TABLE IF EXISTS counterparty_reference CASCADE;
CREATE TABLE counterparty_reference (
 counterparty_identifier TEXT,
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
 accounting_standard TEXT,
 FOREIGN KEY (counterparty_identifier) REFERENCES counterparty_instrument(counterparty_identifier)
);

