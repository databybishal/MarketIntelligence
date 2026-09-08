#!/bin/bash
set -e

echo "Waiting for MSSQL Server to be ready..."

while ! python3 -c "import pyodbc; conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=$MSSQL_SERVER,$MSSQL_PORT;DATABASE=master;UID=$MSSQL_USERNAME;PWD=$MSSQL_SA_PASSWORD;TrustServerCertificate=YES;', timeout=5); conn.close()" 2>/dev/null; do
    echo "MSSQL not ready yet - waiting..."
    sleep 3
done

echo "MSSQL Server is ready!"
