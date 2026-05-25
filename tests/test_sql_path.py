import sys
import os
from dotenv import load_dotenv
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
from src.dbconnect import execute_sql_file
# Optional 1: Use environment variable (recommended)
password = os.getenv('MSSQL_SA_PASSWORD')
if not password:
    raise ValueError("MSSQL_SA_PASSWORD not set in environment")


#Connecting string using Driver 18
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=localhost,1433;"
    f"DATABASE=master;"
    f"UID=sa;"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)

sql_path = './tests/scripts/test.sql'

if __name__ == "__main__":
    print(datetime.datetime.now())
    execute_sql_file(conn_str, sql_path)

