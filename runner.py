from utils.log import runner_logger as log
from src import DATABASE_CONFIG, execute_sql_file
from datetime import datetime


mssql_db = DATABASE_CONFIG['mssql-database']

conn_str = (
    f"DRIVER={mssql_db['driver']};"
    f"SERVER={mssql_db['server']},{mssql_db['port']};"
    f"DATABASE={mssql_db['database']};"
    f"UID={mssql_db['username']};"
    f"PWD={mssql_db['password']};"
    "TrustServerCertificate=YES;"
)

SQL_SCRIPTS = {
    'init_database': './scripts/init_database.sql',
    'bronze_table': './scripts/bronze/bronze_tables.sql'
}


if __name__ == '__main__':
    log.info("Starting Datawarehouse setup...")
        
    try:
        # Init Database
        log.info("Running: init_database")
        execute_sql_file(conn_str, SQL_SCRIPTS['init_database'])
        log.info("Completed: init_database")



        #Bronze layer
        log.info("Running: bronze_table")
        execute_sql_file(conn_str, SQL_SCRIPTS['bronze_table'])
        log.info("Completed: bronze_table")
        
        log.info("All scripts completed successfully")
    except Exception as e:
        log.error(f"Script failed: {e}", exc_info=True)
        raise






