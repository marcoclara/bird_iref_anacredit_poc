-- =============================================================================
-- BIRD & IReF
-- Data Model Definition & Implementation for BIRD and IReF Framework Enablement
-- Universidade Aberta - MEIW - Marco Clara (nº 2302597)
-- =============================================================================

DROP VIEW IF EXISTS ROL_Counterparty CASCADE;
DROP VIEW IF EXISTS ROL_Instrument CASCADE;
DROP VIEW IF EXISTS ROL_Contract CASCADE;
DROP VIEW IF EXISTS ROL_Protection CASCADE;
DROP VIEW IF EXISTS ROL_InterestRateTerms CASCADE;
DROP VIEW IF EXISTS ROL_Accounting CASCADE;

-- =============================================================================
-- ROL Counterparty View
-- Filters legal entities and selects reporting attributes
-- =============================================================================
CREATE OR REPLACE VIEW ROL_Counterparty AS
SELECT
  CounterpartyIdentifier,
  LEI,
  SectorCode,
  ResidencyCountry,
  NACECode
FROM EIL_Counterparty
WHERE CounterpartyType = 'LE';

-- =============================================================================
-- ROL Instrument View
-- Filters active instruments and calculates remaining maturity
-- =============================================================================
CREATE OR REPLACE VIEW ROL_Instrument AS
SELECT
  InstrumentIdentifier,
  InstrumentType,
  Currency,
  MaturityDate,
  RemainingMaturity
FROM EIL_Instrument
WHERE RemainingMaturity > 0;

-- =============================================================================
-- ROL Contract View
-- Filters active contracts for reporting
-- =============================================================================
CREATE OR REPLACE VIEW ROL_Contract AS
SELECT
  ContractIdentifier,
  CounterpartyIdentifier,
  InstrumentIdentifier,
  ContractDate,
  ContractStatus
FROM EIL_Contract
WHERE ContractStatus = 'Performing';

-- =============================================================================
-- ROL Protection View
-- Filters guarantees with positive amounts
-- =============================================================================
CREATE OR REPLACE VIEW ROL_Protection AS
SELECT
  ProtectionIdentifier,
  ContractIdentifier,
  ProtectionType,
  ProtectionAmount
FROM EIL_Guarantee
WHERE ProtectionAmount > 0;

-- =============================================================================
-- ROL Interest Rate Terms View
-- No filtering; assumes all terms are relevant
-- =============================================================================
CREATE OR REPLACE VIEW ROL_InterestRateTerms AS
SELECT
  RateTermIdentifier,
  InstrumentIdentifier,
  RateType,
  ReferenceRate,
  Spread
FROM EIL_InterestRateTerms;

-- =============================================================================
-- ROL Accounting Data View
-- Filters contracts with outstanding balances
-- =============================================================================
CREATE OR REPLACE VIEW ROL_Accounting AS
SELECT
  AccountingIdentifier,
  ContractIdentifier,
  AmountOutstanding,
  AmountInArrears,
  ProvisionAmount,
  WriteOffAmount
FROM EIL_AccountingData
WHERE AmountOutstanding > 0;
