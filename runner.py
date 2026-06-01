from utils.log import runner_logger as log
from src import DATABASE_CONFIG, execute_sql_file
from src.data_ingestion import data_ingestion_run
from src.transformation import data_transformation_run
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
    'bronze_table': './scripts/bronze/bronze_tables.sql',
    'silver_table': './scripts/silver/silver_table.sql'
}


if __name__ == '__main__':
    log.info("Starting Datawarehouse setup...")
        
    try:
        # Init Database
        log.info("Running: init_database")
        master_conn_str = conn_str.replace(
        f"DATABASE={mssql_db['database']};",
        "DATABASE=master;")
        execute_sql_file(master_conn_str, SQL_SCRIPTS['init_database'])
        log.info("Completed: init_database")



        #Bronze layer - DDL
        log.info("Running: bronze_table")
        execute_sql_file(conn_str, SQL_SCRIPTS['bronze_table'])
        log.info("Completed: bronze_table")


        # Bronze layer - ingestion
        log.info("Ingestining: data into Bronze layer")
        data_ingestion_run(conn_str)


        #Silver layer - DDL
        log.info("Running: silver_table")
        execute_sql_file(conn_str, SQL_SCRIPTS['silver_table'])
        log.info("Completed: silver_table")

        # Silver layer - transformation
        log.info("Transformation: transformation data into Silver layer")
        data_transformation_run(conn_str)
        log.info("Completed: Transformation silver layer")


        log.info("All scripts completed successfully")
    except Exception as e:
        log.error(f"Script failed: {e}", exc_info=True)
        raise

    

        






