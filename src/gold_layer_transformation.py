import pyodbc
from utils.log import gold_layer_transformation_logger as log

def gold_layer_transformation_run(conn_str):
    try:
        log.info("Data fetching from silver layer")
        with pyodbc.connect(conn_str) as conn:
            _create_view_gold(conn)
        log.info("Gold layer view created successfully")
    except Exception as e:
        log.exception(f"Transformation failed: {e}")
        raise


def _create_view_gold(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()
    log.info("Creating gold layer view")

    cursor.execute(
        """
            IF OBJECT_ID('gold.fact_IBM_stock_price', 'V') IS NOT NULL
                DROP VIEW gold.fact_IBM_stock_price;
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE VIEW gold.fact_IBM_stock_price AS
            SELECT 
                [date] AS trade_date,
                [open] AS open_price,
                [high] AS high_price,
                [low] AS low_price,
                [close] AS close_price,
                [volume] AS trade_volume,
                ROUND(([high] - [low]), 4) AS daily_range,
                ROUND(
                        ISNULL(
                            ([close] - LAG([close]) OVER(ORDER BY [date])) / 
                            NULLIF(
                                LAG([close]) OVER(ORDER BY [date]), 
                            0), 
                        0), 
                    6)  AS   daily_return,
                CASE 
                    WHEN [close] > [open] THEN 'YES'
                    ELSE 'NO'
                END AS is_green_candle
            FROM silver.IBM_stock_price
        """
    )
    conn.commit()
    cursor.close()

