import pyodbc
import logging
import re
from pathlib import Path
from utils.removeSqlComments import remove_sql_comments

log = logging.getLogger("script") 


def execute_sql_file(conn_str, sql_file_path):
    sql_path = Path(sql_file_path)
    if not sql_path.is_file():
        log.error(f"File not found: {sql_file_path}")
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
    
    with open(sql_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
    
    sql_script = remove_sql_comments(sql_script)
    batches = re.split(r'^\s*GO\s*$', sql_script, flags=re.IGNORECASE | re.MULTILINE)  

    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    try:
        for num,  batch in enumerate(batches, start=1):
            if batch.strip():
                log.info(f"Batch {num}:\n{batch.strip()}\n")
                try:
                    cursor.execute(batch)
                    log.info(f"Batch {num} OK")
                except pyodbc.Error as e:
                    log.error(f"Batch {num} FAILED:\n{e}")
                    raise
                if cursor.description:
                    for row in cursor.fetchall():
                        log.info(f"Row: {row}")
        log.info("All batches executed successfully.")
    except pyodbc.Error as e:
        log.error(f"SQL ERROR: {e}", exc_info=True)
        raise
    finally:
        conn.close()
        