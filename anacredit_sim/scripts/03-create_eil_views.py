################################################################################
# BIRD & IReF
# Data Model Definition & Implementation for BIRD and IReF Framework Enablement
# Universidade Aberta - MEIW - Marco Clara (nº 2302597)
################################################################################

import psycopg2
from psycopg2 import sql
import configparser

# Load database configuration from properties file
config = configparser.ConfigParser()
config.read('anacredit_sim/database/db_config.properties')

host = config.get('database', 'host')
port = config.get('database', 'port')
user = config.get('database', 'user')
password = config.get('database', 'password')
new_db_name = config.get('database', 'new_db_name')

sql_script_path = 'anacredit_sim/database/eil_views.sql'

# Connect to the database
conn = psycopg2.connect(dbname=new_db_name, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Execute the SQL script to create tables
with open(sql_script_path, 'r') as f:
    sql_script = f.read()
    cur.execute(sql_script)
    print("✅ SQL script executed successfully.")

# Commit changes and close connections
conn.commit()
cur.close()
conn.close()