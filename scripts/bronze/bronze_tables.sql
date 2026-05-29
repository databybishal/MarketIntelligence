/********************************************************************
-- Script: Bronze Layer - IBM Stock Price Table
-- Description: Drops (if exists) and recreates the
--              'bronze.IBM_stock_price_data' table in the
--              MarketIntelligenceDWH database.
-- WARNING: Running this script will permanently delete the
--          existing table and all its data if it exists.
********************************************************************/
USE MarketIntelligenceDWH;
GO

IF OBJECT_ID('bronze.IBM_stock_price_data') IS NOT NULL
    DROP TABLE bronze.IBM_stock_price_data;
GO

CREATE TABLE bronze.IBM_stock_price_data (
    [date] NVARCHAR(50),
    [open] NVARCHAR(50),
    [high] NVARCHAR(50),
    [low] NVARCHAR(50),
    [close] NVARCHAR(50),
    [volume] NVARCHAR(50)
);
GO