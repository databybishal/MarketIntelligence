import pyodbc 
import os 
import sys
import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import execute_sql_file
from utils import removeSqlComments


#Load env 
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
password = os.getenv('MSSQL_SA_PASSWORD')
if not password:
    raise ValueError('MSSQL_SA_PASSWORD not set in environment')

#Connecting string using Driver 18
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"
    "UID=sa;"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

# Option 1: Use autocommit=True (recommended for DDL)
conn = pyodbc.connect(conn_str, autocommit=True)

try:
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print("Connected successfully")
    print(f"SQL Server version: {version[:80]}...")
    print(datetime.datetime.today())
    cursor.execute("DROP DATABASE IF EXISTS testDatabase")
    print("Database 'testDatabase' Dropped")
    cursor.execute("CREATE DATABASE testDatabase")
    print("Database 'testDatabase' created")
    print("Test is successfull")

except pyodbc.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()


