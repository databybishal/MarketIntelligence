IF OBJECT_ID('silver.IBM_stock_price', 'U') IS NOT NULL
    DROP TABLE silver.IBM_stock_price;
GO

CREATE TABLE silver.IBM_stock_price(
    id              INT,
    [open]          DECIMAL(10, 4),
    [high]          DECIMAL(10, 4),
    [low]           DECIMAL(10, 4),
    [close]         DECIMAL(10, 4),
    [volume]        BIGINT,
    [date]          DATE,
    dwh_create_date DATETIME2 DEFAULT GETDATE()
);
