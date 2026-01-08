-- =============================================================================
-- BIRD & IReF
-- Data Model Definition & Implementation for BIRD and IReF Framework Enablement
-- Universidade Aberta - MEIW - Marco Clara (nº 2302597)
-- =============================================================================

DROP VIEW IF EXISTS EIL_Instrument CASCADE;
DROP VIEW IF EXISTS EIL_Counterparty CASCADE;
DROP VIEW IF EXISTS EIL_Contract CASCADE;
DROP VIEW IF EXISTS EIL_Guarantee CASCADE;
DROP VIEW IF EXISTS EIL_InterestRateTerms CASCADE;
DROP VIEW IF EXISTS EIL_AccountingData CASCADE;

-- =============================================================================
-- EIL Instrument View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Instrument AS
SELECT
  instrument_id AS InstrumentIdentifier,
  instrument_type AS InstrumentType,
  currency_code AS Currency,
  maturity_date AS MaturityDate,
  interest_rate_type AS InterestRateType,
  reference_rate AS ReferenceRate,
  spread AS Spread,
  maturity_date - CURRENT_DATE AS RemainingMaturity
FROM Instrument;

-- =============================================================================
-- EIL Counterparty View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Counterparty AS
SELECT
  counterparty_id AS CounterpartyIdentifier,
  name AS CounterpartyName,
  legal_entity_identifier AS LEI,
  sector_code AS SectorCode,
  CASE WHEN is_household THEN 'HH' ELSE 'LE' END AS CounterpartyType,
  residency_country_code AS ResidencyCountry,
  nace_code AS NACECode
FROM Counterparty;

-- =============================================================================
-- EIL Contract View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Contract AS
SELECT
  contract_id AS ContractIdentifier,
  counterparty_id AS CounterpartyIdentifier,
  instrument_id AS InstrumentIdentifier,
  contract_date AS ContractDate,
  contract_status AS ContractStatus
FROM Contract;

-- =============================================================================
-- EIL Guarantee View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Guarantee AS
SELECT
  guarantee_id AS ProtectionIdentifier,
  contract_id AS ContractIdentifier,
  guarantee_type AS ProtectionType,
  guarantee_amount AS ProtectionAmount
FROM Guarantee;

-- =============================================================================
-- EIL Interest Rate Terms View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_InterestRateTerms AS
SELECT
  rate_term_id AS RateTermIdentifier,
  instrument_id AS InstrumentIdentifier,
  rate_type AS RateType,
  reference_rate AS ReferenceRate,
  spread AS Spread
FROM InterestRateTerms;

-- =============================================================================
-- EIL Accounting Data View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_AccountingData AS
SELECT
  accounting_id AS AccountingIdentifier,
  contract_id AS ContractIdentifier,
  outstanding_amount AS AmountOutstanding,
  arrears_amount AS AmountInArrears,
  provision_amount AS ProvisionAmount,
  write_off_amount AS WriteOffAmount
FROM accountingdata