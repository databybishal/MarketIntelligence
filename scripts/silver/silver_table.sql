IF OBJECT_ID('silver.IBM_stock_price', 'U') IS NOT NULL
    DROP TABLE silver.IBM_stock_price;
GO

CREATE TABLE silver.IBM_stock_price(   
    [date]          DATE        NOT NULL,       
    [open]          FLOAT       NOT NULL,
    [high]          FLOAT       NOT NULL,
    [low]           FLOAT       NOT NULL,
    [close]         FLOAT       NOT NULL,
    [volume]        BIGINT      NOT NULL,
    dwh_create_date DATETIME2 DEFAULT GETDATE(),
    PRIMARY KEY([date])
);
GO
