import pyodbc
import pandas as pd
from src.apiSource.data_source import source
from utils import extractApis 
from utils.log import ingestion_logger as log
from src.config import DATABASE_CONFIG

symbol = DATABASE_CONFIG['mssql-database'].get('symbol', 'IBM')
api = source['stock_price_apis']['api']

def data_ingestion_run(conn_str):
    try:
        log.info("Fetching data from API source")
        data = extractApis(api)

        if not data:
            raise ValueError("extractApis() returned empty — check API key or network")

        if 'Time Series (Daily)' not in data:
            raise ValueError(f"Unexpected API response structure: {list(data.keys())}")
        
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
            cursor.execute(f"TRUNCATE TABLE bronze.{symbol}_stock_price;")
            cursor.executemany(
                """
                INSERT INTO bronze.{symbol}_stock_price ([date], [open], [high], [low], [close], [volume])
                VALUES(?, ?, ?, ?, ?, ?)
                """.format(symbol=symbol),
                df.values.tolist()
            )
            conn.commit()
        log.info(f"Ingested {len(df)} rows into bronze.{symbol}_stock_price")
    except Exception as e:
        log.exception(f"Ingestion failed: {e}")
        raise



