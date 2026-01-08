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

sql_script_path = 'anacredit_sim/database/db_tables.sql'

# Connect to the default 'postgres' database for administrative tasks
conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
conn.autocommit = True
cur = conn.cursor()

# Check if the database already exists
cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (new_db_name,))
exists = cur.fetchone()

# If it exists, terminate active connections and drop it
if exists:
    cur.execute(sql.SQL("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s"), [new_db_name])
    cur.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(new_db_name)))
    print(f"✅ Database '{new_db_name}' dropped successfully.")

# Create the new database
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
print(f"✅ Database '{new_db_name}' created successfully.")

# Close connection to the default database
cur.close()
conn.close()

# Connect to the newly created database
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