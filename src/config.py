import os 

DATABASE_CONFIG = {
    "mssql-database": {
        "server": "localhost,1433",
        "database": "master",
        "username": "sa",
        "password": os.getenv("MSSQL_SA_PASSWORD"),
        "driver": "{ODBC Driver 18 for SQL Server}"
    },
}