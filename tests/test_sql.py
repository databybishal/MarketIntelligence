import pyodbc
import os 

# Optional 1: Use environment variable (recommended)
password = os.getenv('MSSQL_SA_PASSWORD', 'Bishalkoirala@1212')


#Connecting string using Driver 18
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost, 1433;"
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
    # Optional: create your market intelligence database
    cursor.execute("CREATE DATABASE testDatabase")
    print("Database 'testDatabase' created")

except pyodbc.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()


