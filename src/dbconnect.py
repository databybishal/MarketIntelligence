import pyodbc
import re
from utils.removeSqlComments import remove_sql_comments




def execute_sql_file(conn_str, sql_file_path):

    """
    Reads a .sql.file and executes its content.

    Args:
        conn_str = ODBC connection string
        sql_file_path: path to the .sql file(e.g., 'script/create_tables.sql')
    """

    #Read teh SQL_file
    try:

        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
    except FileNotFoundError as e:
        print(f"File not found: {sql_file_path}")
        print(f"Full error: {e}")
        return
    
    sql_script = remove_sql_comments(sql_script)

    # Split on lines that contain only "GO" (case-insensitive. optional space)
    batches = re.split(r'^\s*GO\s*$', sql_script, flags=re.IGNORECASE | re.MULTILINE)  

    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    try:
        num = 0
        for batch in batches:
            num += 1
            if batch.strip():
                print(f"Executing batch {num} : \n{batch.strip()[:200]}...\n")
                cursor.execute(batch)
                if cursor.description:
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
        print("All batches executed successfully.")
    except pyodbc.Error as e:
        print(f"SQL ERROR: {e}")
        raise
    finally:
        conn.close()