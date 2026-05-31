import os
import sys
import logging
import pandas as pd
from apiSource.data_source import source


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import extractApis


log = logging.getLogger('ingestion')
api = source['stock_price_apis']['api']

if __name__ == '__main__':
    try:
        log.info("Preparing for data ingestion")
        data = extractApis(api)
        time_series = data['Time Series (Daily)']
        df = pd.DataFrame(
            [
                {
                    'date': date,
                    'open': value['1. open'],
                    'high': value['2. high'],
                    'low': value['3. low'],
                    'close': value['4. close'],
                    'volume': value['5. volume']
                }
                for date, value in time_series.items()
            ]
        )
        print(df.head())
    except Exception as e:
        pass
    



