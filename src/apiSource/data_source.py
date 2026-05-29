import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


stock_price_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
symbol = os.getenv('STOCK_PRICE_API_SYMBOL')
interval = os.getenv('STOCK_PRICE_API_INTERVAL')
function = os.getenv('STOCK_PRICE_API_FUNCTION')



source = {
    'stock_price_apis' : {
        'api': f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={stock_price_api_key}',
    },
}

