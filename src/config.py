import os 
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
server = os.getenv('SERVER')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv("MSSQL_SA_PASSWORD")
driver = os.getenv('DRIVER')
# print(server, port, database, username, password, driver) # for check

DATABASE_CONFIG = {
    "mssql-database": {
        'server': server,
        'port': port,
        'database': database,
        'username': username,
        'password': password,
        'driver': driver
    },
}
# print(DATABASE_CONFIG['mssql-database']) #for check