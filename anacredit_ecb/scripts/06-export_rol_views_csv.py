################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import psycopg2
import pandas as pd
import os
import configparser

# Load database configuration from properties file
config = configparser.ConfigParser()
config.read('anacredit_ecb/database/db_config.properties')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname = config.get('database', 'new_db_name'),
    user = config.get('database', 'user'),
    password = config.get('database', 'password'),
    host = config.get('database', 'host'),
    port = config.get('database', 'port')
)

# Output path to ROL CSV files
output_path = "anacredit_ecb/output/csv/rol"

# List of views to export
views = [
    "ROL_Counterparty",
    "ROL_Instrument",
    "ROL_Contract",
    "ROL_Protection",
    "ROL_InterestRateTerms",
    "ROL_Accounting"
]

# Export each view to specified folder
for view in views:
    df = pd.read_sql(f"SELECT * FROM {view}", conn)
    csv_file = os.path.join(output_path, f"{view}.csv")
    df.to_csv(csv_file, index=False)
    print(f"✅ Exported: {csv_file}")

conn.close()
