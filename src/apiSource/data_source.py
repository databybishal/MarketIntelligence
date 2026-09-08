from src.config import DATABASE_CONFIG

stock_price_api_key = DATABASE_CONFIG['mssql-database'].get('api_key')
symbol = DATABASE_CONFIG['mssql-database'].get('symbol', 'IBM')
interval = DATABASE_CONFIG['mssql-database'].get('interval', '5min')
function = DATABASE_CONFIG['mssql-database'].get('function', 'TIME_SERIES_DAILY')

source = {
    'stock_price_apis' : {
        'api': f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={stock_price_api_key}',
    },
}



