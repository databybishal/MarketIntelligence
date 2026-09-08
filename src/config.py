import os 
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
server = os.getenv('SERVER')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv("MSSQL_SA_PASSWORD")
driver = os.getenv('DRIVER')
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
symbol = os.getenv('STOCK_PRICE_API_SYMBOL', 'IBM')
interval = os.getenv('STOCK_PRICE_API_INTERVAL', '5min')
function = os.getenv('STOCK_PRICE_API_FUNCTION', 'TIME_SERIES_DAILY')

DATABASE_CONFIG = {
    "mssql-database": {
        'server': server,
        'port': port,
        'database': database,
        'username': username,
        'password': password,
        'driver': driver,
        'api_key': api_key,
        'symbol': symbol,
        'interval': interval,
        'function': function,
    },
}
# print(DATABASE_CONFIG['mssql-database']) #for check