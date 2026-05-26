import sys
import os
from dotenv import load_dotenv
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

#importing the 
from src import execute_sql_file, DATABASE_CONFIG

# Optional 1: Use environment variable (recommended)
password = os.getenv('MSSQL_SA_PASSWORD')
if not password:
    raise ValueError("MSSQL_SA_PASSWORD not set in environment")

mssql = DATABASE_CONFIG['mssql-database']


#Connecting string using Driver 18
conn_str = (
    f"DRIVER={mssql['driver']};"
    f"SERVER={mssql['server']},{mssql['port']};"
    f"DATABASE={mssql['database']};"
    f"UID={mssql['username']};"
    f"PWD={mssql['password']};"
    f"TrustServerCertificate=yes;"
)


# ✅ Simple relative path
sql_path = 'tests/scripts/test_executePath.sql'

if __name__ == "__main__":
    print(datetime.datetime.now())
    execute_sql_file(conn_str, sql_path)

