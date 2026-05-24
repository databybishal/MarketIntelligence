/********************************************************************
-- Script: Setup DataWarehouse Database
-- Description: Drops and recreates the 'MarketIntelligenceDWH' database
--              and creates the bronze, silver, and gold schemas.
-- WARNING: Running this script will permanently delete the existing
--          DataWarehouse database if it exists.
********************************************************************/

-- Switch to master database to manage databases
USE master;
GO

-- Drop existing DataWarehouse database if it exists
IF EXISTS(SELECT 1 FROM sys.databases WHERE name = 'MarketIntelligenceDWH')
BEGIN
    ALTER DATABASE MarketIntelligenceDWH
    SET SINGLE_USER
    WITH ROLLBACK IMMEDIATE;
    DROP DATABASE MarketIntelligenceDWH;
END;

-- Create a new DataWarehouse database
CREATE DATABASE MarketIntelligenceDWH;
GO

-- Switch to the new database
USE MarketIntelligenceDWH;
GO

-- Create ETL layer schemas
CREATE SCHEMA bronze;
GO

CREATE SCHEMA sliver;
GO

CREATE SCHEMA gold;
GO