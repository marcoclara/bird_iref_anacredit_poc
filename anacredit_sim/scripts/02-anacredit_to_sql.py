################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

from faker import Faker
import psycopg2
import random
from datetime import datetime, timedelta
import configparser

# Initialize Faker
fake = Faker()

# Load database configuration from properties file
config = configparser.ConfigParser()
config.read('anacredit_sim/database/db_config.properties')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname = config.get('database', 'new_db_name'),
    user = config.get('database', 'user'),
    password = config.get('database', 'password'),
    host = config.get('database', 'host'),
    port = config.get('database', 'port')   
)
cursor = conn.cursor()

# Store IDs for foreign key relationships
counterparty_ids = []
instrument_ids = []
contract_ids = []

# Generate Counterparty Data
for _ in range(100):
    name = fake.name()
    lei = fake.bothify(text='????????????????????')  # Simulated LEI
    sector = random.choice(['NFC', 'HH', 'GOV'])
    country = fake.country_code()
    nace = fake.bothify(text='??.??')
    is_household = sector == 'HH'

    cursor.execute("""
        INSERT INTO Counterparty (name, legal_entity_identifier, sector_code, residency_country_code, nace_code, is_household)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING counterparty_id
    """, (name, lei, sector, country, nace, is_household))
    counterparty_ids.append(cursor.fetchone()[0])

# Generate Instrument Data
for _ in range(100):
    instrument_type = random.choice(['Loan', 'Overdraft', 'Credit Line'])
    currency = random.choice(['EUR', 'USD', 'GBP'])
    maturity = datetime.now() + timedelta(days=random.randint(30, 3650))
    rate_type = random.choice(['Fixed', 'Variable'])
    ref_rate = random.choice(['EURIBOR', 'LIBOR', 'SOFR'])
    spread = round(random.uniform(0.5, 5.0), 2)

    cursor.execute("""
        INSERT INTO Instrument (instrument_type, currency_code, maturity_date, interest_rate_type, reference_rate, spread)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING instrument_id
    """, (instrument_type, currency, maturity, rate_type, ref_rate, spread))
    instrument_ids.append(cursor.fetchone()[0])

# Generate Contract Data
for _ in range(100):
    counterparty_id = random.choice(counterparty_ids)
    instrument_id = random.choice(instrument_ids)
    contract_date = datetime.now() - timedelta(days=random.randint(0, 3650))
    status = random.choice(['Performing', 'Non-performing'])

    cursor.execute("""
        INSERT INTO Contract (counterparty_id, instrument_id, contract_date, contract_status)
        VALUES (%s, %s, %s, %s) RETURNING contract_id
    """, (counterparty_id, instrument_id, contract_date, status))
    contract_ids.append(cursor.fetchone()[0])

# Generate Guarantee Data
for contract_id in random.sample(contract_ids, 50):  # Only some contracts have guarantees
    guarantee_type = random.choice(['Mortgage', 'Pledge', 'Personal Guarantee'])
    amount = round(random.uniform(1000, 100000), 2)

    cursor.execute("""
        INSERT INTO Guarantee (contract_id, guarantee_type, guarantee_amount)
        VALUES (%s, %s, %s)
    """, (contract_id, guarantee_type, amount))

# Generate Interest Rate Terms
for instrument_id in instrument_ids:
    rate_type = random.choice(['Fixed', 'Variable'])
    ref_rate = random.choice(['EURIBOR', 'LIBOR', 'SOFR'])
    spread = round(random.uniform(0.5, 5.0), 2)

    cursor.execute("""
        INSERT INTO InterestRateTerms (instrument_id, rate_type, reference_rate, spread)
        VALUES (%s, %s, %s, %s)
    """, (instrument_id, rate_type, ref_rate, spread))

# Generate Accounting Data
for contract_id in contract_ids:
    outstanding = round(random.uniform(1000, 500000), 2)
    # arrears = round(random.uniform(0, 5000), 2)
    arrears = round(random.uniform(0, outstanding), 2)  # Ensure arrears ≤ outstanding
    provision = round(random.uniform(0, 10000), 2)
    write_off = round(random.uniform(0, 2000), 2)

    cursor.execute("""
        INSERT INTO AccountingData (contract_id, outstanding_amount, arrears_amount, provision_amount, write_off_amount)
        VALUES (%s, %s, %s, %s, %s)
    """, (contract_id, outstanding, arrears, provision, write_off))

# Finalize
conn.commit()
cursor.close()
conn.close()
print("Synthetic data generation complete.")