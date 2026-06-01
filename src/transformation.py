import os 
import sys
import pyodbc
import logging
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.log import transformation_logger as log

def data_transformation_run(conn_str):
    try:
        log.info("Data fetching from bronze layer")
        with pyodbc.connect(conn_str) as conn:
            df = pd.read_sql(
                """
                SELECT 
                    [date],
                    [open],
                    [high],
                    [low],
                    [close],
                    [volume]
                FROM bronze.IBM_stock_price;
                """,
                conn
            )
            log.info(f"Fetched {len(df)} rows from bronze layer")
            
            # Transformation
            df = _transform(df)
            log.info("Transformation completed")

            # Load to silver layer
            _load_to_silver(df, conn)
            log.info("Data loaded to silver layer successfully")

            
    except Exception as e:
        log.exception(f"Transformation failed: {e}")
        raise

def _transform(df: pd.DataFrame) -> pd.DataFrame:
    #Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    #parse and sort by date
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    #Drop duplicatess
    df = df.drop_duplicates(subset=["date"])

    #Cast numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    #Drop rows with nulls in critical columns
    critical_cols= ["date", "open", "high", "low", "close", "volume"]
    df = df.dropna(subset=critical_cols)

    

    #Yeti for gold layer views ko laig 
    # Derived features
    # df["daily_return"]   = df["close"].pct_change().round(6)
    # df["daily_range"]    = (df["high"] - df["low"]).round(4)
    # df["is_green_candle"] = (df["close"] > df["open"]).astype(int)

    return df


def _load_to_silver(df: pd.DataFrame, conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE silver.IBM_stock_price")

    rows = [
        (row.date, row.open, row.high, row.low, row.close, int(row.volume))
        for row in df.itertuples(index=False)
    ]

    cursor.executemany(
        """
        INSERT INTO silver.IBM_stock_price
            ([date], [open], [high], [low], [close], [volume])
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()
    log.info(f"Inserted {len(rows)} rows into silver.IBM_stock_price")
