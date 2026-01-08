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
  instrument_identifier AS InstrumentIdentifier,
  type_of_instrument AS InstrumentType,
  currency AS Currency,
  legal_final_maturity_date AS MaturityDate,
  interest_rate_type AS InterestRateType,
  reference_rate AS ReferenceRate,
  interest_rate_spreadmargin AS Spread,
  legal_final_maturity_date - CURRENT_DATE AS RemainingMaturity
FROM Instrument;

-- =============================================================================
-- EIL Counterparty View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Counterparty AS
SELECT
  counterparty_identifier AS CounterpartyIdentifier,
  name AS CounterpartyName,
  CASE
    WHEN lei = 'nan' THEN 'Non-applicable'
    ELSE lei END AS LEI,
  CASE
    WHEN institutional_sector LIKE 'S.11%' THEN 'NFC'
    WHEN institutional_sector LIKE 'S.12%' THEN 'FC'
    WHEN institutional_sector LIKE 'S.13%' THEN 'GG'
    WHEN institutional_sector LIKE 'S.14%' THEN 'HH'
    WHEN institutional_sector LIKE 'S.15%' THEN 'NPISH'
    ELSE 'RoW' END AS SectorCode,
  CASE
    WHEN institutional_sector LIKE 'S.11%' THEN 'LE'
    WHEN institutional_sector LIKE 'S.12%' THEN 'LE'
    WHEN institutional_sector LIKE 'S.13%' THEN 'GG'
    WHEN institutional_sector LIKE 'S.14%' THEN 'HH'
    WHEN institutional_sector LIKE 'S.15%' THEN 'LE,IG'
    ELSE 'LE,IG,HH' END AS CounterpartyType,
  address_country AS ResidencyCountry,
  NULL AS NACECode
FROM counterparty_reference;

-- =============================================================================
-- EIL Contract View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Contract AS
SELECT
  ci.contract_identifier || '_' || ci.counterparty_role AS ContractIdentifier,
  ci.counterparty_identifier AS CounterpartyIdentifier,
  ci.instrument_identifier AS InstrumentIdentifier,
  -- contract date derived from multiple attributes
  CASE
    WHEN f.default_status_of_the_instrument IS NOT NULL 
         AND f.default_status_of_the_instrument NOT IN ('Not in default', 'Non-applicable') THEN CAST(f.date_of_the_default_status_of_the_instrument AS DATE)
    WHEN a.performing_status_of_the_instrument = 'Non-performing' THEN NULL
    WHEN a.status_of_forbearance_and_renegotiation IN ('Forborne', 'Renegotiated') THEN a.date_of_the_status_of_forbearance_and_renegotiation
    ELSE a.date_of_the_performing_status_of_the_instrument
  END AS ContractDate,
  -- contract state derived from multiple attributes
  CASE
    WHEN f.default_status_of_the_instrument IS NOT NULL 
         AND f.default_status_of_the_instrument NOT IN ('Not in default', 'Non-applicable') THEN 'Defaulted'
    WHEN a.performing_status_of_the_instrument = 'Non-performing' THEN 'Non-performing'
    WHEN a.status_of_forbearance_and_renegotiation IN ('Forborne', 'Renegotiated') THEN 'Forborne/Renegotiated'
    ELSE 'Performing'
  END AS ContractStatus
FROM counterparty_instrument ci
LEFT JOIN instrument i ON ci.instrument_identifier = i.instrument_identifier
LEFT JOIN financial f ON ci.instrument_identifier = f.instrument_identifier
LEFT JOIN accounting a ON ci.instrument_identifier = a.instrument_identifier
WHERE ci.reporting_reference_date = i.reporting_reference_date
AND ci.reporting_reference_date = f.reporting_reference_date
AND ci.reporting_reference_date = a.reporting_reference_date;

-- =============================================================================
-- EIL Guarantee View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_Guarantee AS
SELECT DISTINCT
  pr.protection_identifier AS ProtectionIdentifier,
  ipr.contract_identifier AS ContractIdentifier,
  pr.type_of_protection AS ProtectionType,
  ipr.protection_allocated_value AS ProtectionAmount
FROM instrument_protection_received ipr
JOIN protection_received pr
  ON ipr.protection_identifier = pr.protection_identifier
WHERE ipr.reporting_reference_date = pr.reporting_reference_date;

-- =============================================================================
-- EIL Interest Rate Terms View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_InterestRateTerms AS
SELECT
  reporting_reference_date || '_' || reporting_agent_identifier || '_' || instrument_identifier AS RateTermIdentifier,
  instrument_identifier AS InstrumentIdentifier,
  interest_rate_type AS RateType,
  reference_rate AS ReferenceRate,
  interest_rate_spreadmargin AS Spread
FROM instrument;

-- =============================================================================
-- EIL Accounting Data View
-- =============================================================================
CREATE OR REPLACE VIEW EIL_AccountingData AS
SELECT
  a.reporting_reference_date || '_' || a.reporting_agent_identifier || '_' || a.instrument_identifier AS AccountingIdentifier,
  a.contract_identifier AS ContractIdentifier,
  f.outstanding_nominal_amount AS AmountOutstanding,
  f.arrears_for_the_instrument AS AmountInArrears,
  CASE WHEN a.accumulated_impairment_amount IS NULL THEN 0
  ELSE a.accumulated_impairment_amount END AS ProvisionAmount,
  CASE WHEN a.accumulated_writeoffs IS NULL THEN 0
  ELSE a.accumulated_writeoffs END AS WriteOffAmount
FROM accounting a
LEFT JOIN financial f
  ON a.instrument_identifier = f.instrument_identifier
WHERE a.reporting_reference_date = f.reporting_reference_date;
