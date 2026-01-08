-- =============================================================================
-- BIRD & IReF
-- Data Model Definition & Implementation for BIRD and IReF Framework Enablement
-- Universidade Aberta - MEIW - Marco Clara (nº 2302597)
-- =============================================================================

-- =============================================================================
-- COUNTERPARTY TABLE
-- Stores information about borrowers (individuals or legal entities)
-- Includes identifiers, sector classification, and residency
-- =============================================================================
CREATE TABLE Counterparty (
    counterparty_id SERIAL PRIMARY KEY, -- Unique ID for each counterparty
    name VARCHAR(255) NOT NULL, -- Legal or individual name
    legal_entity_identifier VARCHAR(20), -- LEI for legal entities (if applicable)
    sector_code VARCHAR(10), -- Sector classification (e.g., NFC, HH)
    residency_country_code CHAR(2), -- ISO country code of residency
    nace_code VARCHAR(10), -- Economic activity code (NACE Rev.2)
    is_household BOOLEAN DEFAULT FALSE -- Flag to identify households
);

-- =============================================================================
-- INSTRUMENT TABLE
-- Represents credit instruments such as loans, credit lines, etc.
-- Includes financial terms and classification
-- =============================================================================
CREATE TABLE Instrument (
    instrument_id SERIAL PRIMARY KEY, -- Unique ID for each instrument
    instrument_type VARCHAR(50) NOT NULL, -- Type of instrument (e.g., loan, overdraft)
    currency_code CHAR(3) NOT NULL, -- ISO currency code (e.g., EUR)
    maturity_date DATE, -- Contractual maturity date
    interest_rate_type VARCHAR(20), -- Fixed or variable rate
    reference_rate VARCHAR(50), -- Reference rate (e.g., EURIBOR)
    spread NUMERIC(5,2) -- Interest rate spread over reference rate
);

-- =============================================================================
-- CONTRACT TABLE
-- Links counterparties to instruments
-- Captures contractual relationships and status
-- =============================================================================
CREATE TABLE Contract (
    contract_id SERIAL PRIMARY KEY, -- Unique ID for each contract
    counterparty_id INT NOT NULL, -- FK to Counterparty
    instrument_id INT NOT NULL, -- FK to Instrument
    contract_date DATE NOT NULL, -- Date contract was signed
    contract_status VARCHAR(20), -- Status (e.g., active, terminated)
    FOREIGN KEY (counterparty_id) REFERENCES Counterparty(counterparty_id),
    FOREIGN KEY (instrument_id) REFERENCES Instrument(instrument_id)
);

-- =============================================================================
-- GUARANTEE TABLE
-- Details of guarantees or collateral linked to contracts
-- Used to assess credit risk mitigation
-- =============================================================================
CREATE TABLE Guarantee (
    guarantee_id SERIAL PRIMARY KEY, -- Unique ID for each guarantee
    contract_id INT NOT NULL, -- FK to Contract
    guarantee_type VARCHAR(50), -- Type of guarantee (e.g., mortgage, pledge)
    guarantee_amount NUMERIC(15,2), -- Value of the guarantee
    FOREIGN KEY (contract_id) REFERENCES Contract(contract_id)
);

-- =============================================================================
-- INTEREST RATE TERMS TABLE
-- Captures detailed interest rate conditions for instruments
-- Useful for understanding pricing and risk
-- =============================================================================
CREATE TABLE InterestRateTerms (
    rate_term_id SERIAL PRIMARY KEY, -- Unique ID for each rate term
    instrument_id INT NOT NULL, -- FK to Instrument
    rate_type VARCHAR(20), -- Fixed or variable
    reference_rate VARCHAR(50), -- Reference rate (e.g., EURIBOR)
    spread NUMERIC(5,2), -- Spread over reference rate
    FOREIGN KEY (instrument_id) REFERENCES Instrument(instrument_id)
);

-- =============================================================================
-- ACCOUNTING DATA TABLE
-- Stores financial metrics for contracts
-- Includes outstanding amounts, arrears, provisions, and write-offs
-- =============================================================================
CREATE TABLE AccountingData (
    accounting_id SERIAL PRIMARY KEY, -- Unique ID for each accounting record
    contract_id INT NOT NULL, -- FK to Contract
    outstanding_amount NUMERIC(15,2), -- Current outstanding balance
    arrears_amount NUMERIC(15,2), -- Amount overdue
    provision_amount NUMERIC(15,2), -- Provisioned amount for credit risk
    write_off_amount NUMERIC(15,2), -- Amount written off
    FOREIGN KEY (contract_id) REFERENCES Contract(contract_id)
);
