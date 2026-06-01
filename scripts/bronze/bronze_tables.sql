IF OBJECT_ID('bronze.IBM_stock_price', 'U') IS NOT NULL
    DROP TABLE bronze.IBM_stock_price;
GO

CREATE TABLE bronze.IBM_stock_price (
    [date] NVARCHAR(50),
    [open] NVARCHAR(50),
    [high] NVARCHAR(50),
    [low] NVARCHAR(50),
    [close] NVARCHAR(50),
    [volume] NVARCHAR(50)
);
GO