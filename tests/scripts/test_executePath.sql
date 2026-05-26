USE master;
GO 

IF EXISTS(SELECT 1 FROM sys.databases WHERE name = 'test_database_dwh')
BEGIN 
    ALTER DATABASE test_database_dwh
    SET SINGLE_USER 
    WITH ROLLBACK IMMEDIATE;
    DROP DATABASE test_database_dwh;
END;
GO

CREATE DATABASE test_database_dwh;
GO 

USE test_database_dwh;
GO 

CREATE SCHEMA test_layer;
GO 

DROP TABLE IF EXISTS test_layer.test_table;
GO 

CREATE TABLE test_layer.test_table (
    ID INT PRIMARY KEY,
    testName VARCHAR(144) 
);
GO 

INSERT INTO test_layer.test_table(ID, testName) VALUES
    (1, 'Sample Data'),
    (2, 'Bishal Koirala'),
    (3, 'Komal Koirala');
GO
