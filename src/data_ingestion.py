import os
import sys
import logging
import pandas as pd
from .apiSource.data_source import source
import pyodbc

# Add project root to path so apiSource can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import extractApis 
from utils.log import ingestion_logger as log

api = source['stock_price_apis']['api']

def data_ingestion_run(conn_str):
    try:
        log.info("Fetching data from API source")
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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO bronze.IBM_stock_price ([date], [open], [high], [low], [close], [volume])
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                df.values.tolist()
            )
            conn.commit()
        log.info(f"Ingested {len(df)} rows into bronze.IBM_stock_price")
    except Exception as e:
        log.exception(f"Ingestion failed: {e}")
        raise



