import datetime
import pandas as pd
from dotenv import load_dotenv

# sys.path.insert(os.path.join(os.path.dirname(__file__), ')
# load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
from src import DATABASE_CONFIG, execute_sql_file

mssql_db = DATABASE_CONFIG['mssql-database']

conn_str = (
    f"DRIVER={mssql_db['driver']};"
    f"SERVER={mssql_db['server']},{mssql_db['port']};"
    f"DATABASE={mssql_db['database']};"
    f"UID={mssql_db['username']};"
    f"PWD={mssql_db['password']};"
    "TrustServerCertificate=YES;"
)

if __name__ == '__main__':

        #############################################################
    # Script: Setup DataWarehouse Database
    # Description: Drops and recreates the 'MarketIntelligenceDWH' database
    #              and creates the bronze, silver, and gold schemas.
    # WARNING: Running this script will permanently delete the existing
    #          DataWarehouse database if it exists.
    #############################################################
    init_database = './scripts/init_database.sql'
    print(datetime.datetime.today())
    execute_sql_file(conn_str, init_database)




        #############################################################
    # Script: Bronze Layer - IBM Stock Price Table
    # Description: Drops (if exists) and recreates the
    #              'bronze.IBM_stock_price_data' table in the
    #              MarketIntelligenceDWH database.
    # WARNING: Running this script will permanently delete the
    #          existing table and all its data if it exists.
    #############################################################
    bronze_table = './scripts/bronze/bronze_tables.sql'
    print(datetime.datetime.today())
    execute_sql_file(conn_str, bronze_table)

    




