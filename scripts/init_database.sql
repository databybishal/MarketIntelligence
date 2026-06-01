
USE master;
GO


IF EXISTS(SELECT 1 FROM sys.databases WHERE name = 'MarketIntelligenceDWH')
BEGIN
    ALTER DATABASE MarketIntelligenceDWH
    SET SINGLE_USER
    WITH ROLLBACK IMMEDIATE;
    DROP DATABASE MarketIntelligenceDWH;
END;


CREATE DATABASE MarketIntelligenceDWH;
GO


USE MarketIntelligenceDWH;
GO


CREATE SCHEMA bronze;
GO

CREATE SCHEMA silver;
GO

CREATE SCHEMA gold;
GO