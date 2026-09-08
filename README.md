# Market Intelligence Data Warehouse

A cloud-native stock price analytics platform built with a **Bronze → Silver → Gold** layered data warehouse architecture on **Microsoft SQL Server**, powered by **Alpha Vantage API** data ingestion.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-darkblue)
![Docker](https://img.shields.io/badge/Docker-%232496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Architecture Overview

The project implements a **Medallion Architecture** pattern with three distinct data layers:

```
┌─────────────────────────────────────────────────────────┐
│                    GOLD LAYER                            │
│  ┌──────────────────────┐                               │
│  │  fact_IBM_stock_price│  ← Aggregated views with      │
│  │  (View)              │    derived metrics (daily      │
│  │                      │    return, daily_range,        │
│  │                      │    is_green_candle)            │
│  └──────────────────────┘                               │
├─────────────────────────────────────────────────────────┤
│                  SILVER LAYER                            │
│  ┌──────────────────────┐                               │
│  │  IBM_stock_price     │  ← Cleaned, typed,            │
│  │  (Table)             │    deduplicated, sorted       │
│  └──────────────────────┘                               │
├─────────────────────────────────────────────────────────┤
│                  BRONZE LAYER                            │
│  ┌──────────────────────┐                               │
│  │  IBM_stock_price     │  ← Raw API landing zone       │
│  │  (Table)             │    as NVARCHAR                │
│  └──────────────────────┘                               │
├─────────────────────────────────────────────────────────┤
│                  API SOURCE                              │
│  ┌──────────────────────┐                               │
│  │  Alpha Vantage API   │  ← Daily stock price data     │
│  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
```

---

## Features

- **Automated ETL Pipeline** — End-to-end data ingestion, transformation, and aggregation driven by a single runner
- **3-Layer Medallion Architecture** — Bronze (raw), Silver (cleaned), Gold (business-ready views)
- **Dockerized MSSQL Server** — Consistent database environment via `docker compose`
- **Structured Logging** — Per-module log files with rotation (5 most recent retained)
- **Configurable Symbol** — Switch stock symbols via environment variables without code changes
- **Derived Analytics** — Daily returns, trading ranges, and green/red candle indicators in the gold layer

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.8+ |
| Docker & Docker Compose | 20.10+ |
| Microsoft SQL Server | 2022 (via Docker) |
| ODBC Driver | 18 for SQL Server |

---

## Quick Start

### 1. Clone the Repository

```bash
git clone <repo-url>
cd MarketIntelligence
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# MSSQL Configuration
SERVER=localhost
PORT=1433
DATABASE=MarketIntelligenceDWH
DB_USERNAME=sa
MSSQL_SA_PASSWORD=YourStrong!Password123
DRIVER={ODBC Driver 18 for SQL Server}

# Alpha Vantage API
STOCK_PRICE_API_SYMBOL=IBM
STOCK_PRICE_API_INTERVAL=5min
STOCK_PRICE_API_FUNCTION=TIME_SERIES_DAILY
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

> **⚠️ Never commit your `.env` file.** It is already in `.gitignore`.

### 3. Start MSSQL Server via Docker

```bash
docker compose -f docker/mssql.yaml up -d
```

Verify the container is running:

```bash
docker ps
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Full Pipeline

```bash
python runner.py
```

This executes the complete ETL flow:

1. **Initialize Database** — Creates the `MarketIntelligenceDWH` database with `bronze`, `silver`, and `gold` schemas
2. **Bronze Layer DDL** — Creates the raw landing table
3. **Ingestion** — Fetches data from Alpha Vantage API and loads it into the bronze layer
4. **Silver Layer DDL** — Creates the cleaned table with proper data types
5. **Silver Transformation** — Normalizes columns, parses dates, removes duplicates, casts types
6. **Gold Layer View** — Creates an aggregated view with derived metrics

---

## Project Structure

```
MarketIntelligence/
├── runner.py                      # Main ETL pipeline orchestrator
├── .env                           # Environment variables (never commit)
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
├── docker/
│   └── mssql.yaml                 # Docker Compose for SQL Server
├── scripts/
│   ├── init_database.sql          # Creates database and schemas
│   ├── bronze/
│   │   └── bronze_tables.sql      # Bronze layer DDL
│   ├── silver/
│   │   └── silver_table.sql       # Silver layer DDL
│   └── gold/
│       └── gold_view.sql          # Gold layer view definition
├── src/
│   ├── __init__.py                # Package exports
│   ├── config.py                  # Centralized configuration loader
│   ├── dbconnect.py               # SQL file execution engine
│   ├── data_ingestion.py          # Bronze layer data ingestion
│   ├── silver_layer_transformation.py  # Silver layer transform + load
│   ├── gold_layer_transformation.py    # Gold layer view creation
│   └── apiSource/
│       ├── __init__.py
│       └── data_source.py         # Alpha Vantage API URL builder
├── utils/
│   ├── __init__.py
│   ├── api_extract.py             # HTTP client for API calls
│   ├── log.py                     # Structured logging setup
│   └── removeSqlComments.py       # SQL comment stripper
├── tests/                         # Test scripts and fixtures
│   ├── test_api_extract.py
│   ├── test_sql.py
│   ├── test_sql_path.py
│   ├── test_stock_price_api.py
│   └── scripts/
└── logs/                          # Application log files (auto-managed)
```

---

## Running Individual Components

### Run Only Ingestion (Bronze Layer)

```python
from src.data_ingestion import data_ingestion_run
from src.config import DATABASE_CONFIG

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost,1433;DATABASE=MarketIntelligenceDWH;UID=sa;PWD=your_password;TrustServerCertificate=YES;"
data_ingestion_run(conn_str)
```

### Execute a SQL Script

```python
from src import execute_sql_file, DATABASE_CONFIG

mssql_db = DATABASE_CONFIG['mssql-database']
conn_str = f"DRIVER={mssql_db['driver']};SERVER={mssql_db['server']},{mssql_db['port']};DATABASE={mssql_db['database']};UID={mssql_db['username']};PWD={mssql_db['password']};TrustServerCertificate=YES;"
execute_sql_file(conn_str, './scripts/init_database.sql')
```

---

## Gold Layer View Schema

The `gold.fact_IBM_stock_price` view provides business-ready analytics:

| Column | Type | Description |
|--------|------|-------------|
| `trade_date` | DATE | Trading date |
| `open_price` | FLOAT | Opening price |
| `high_price` | FLOAT | Highest price |
| `low_price` | FLOAT | Lowest price |
| `close_price` | FLOAT | Closing price |
| `trade_volume` | BIGINT | Trading volume |
| `daily_range` | DECIMAL(10,4) | High minus low |
| `daily_return` | DECIMAL(10,6) | Percentage change from previous day |
| `is_green_candle` | VARCHAR(3) | `YES` if close > open, else `NO` |

---

## Logging

The project uses structured logging with per-module log files stored in the `logs/` directory. Each logger rotates and keeps the **5 most recent** log files:

| Logger Name | Log File Prefix |
|-------------|-----------------|
| `runner` | `runner_*.log` |
| `script` | `scripts_*.log` |
| `ingestion` | `ingestion_*.log` |
| `silver_layer_transformation` | `silver_transformation_*.log` |
| `gold_layer_transformation` | `gold_layer_transformation_*.log` |

---

## Configuration Reference

All configuration is managed through environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER` | `localhost` | SQL Server host |
| `PORT` | `1433` | SQL Server port |
| `DATABASE` | `MarketIntelligenceDWH` | Target database name |
| `DB_USERNAME` | `sa` | SQL Server username |
| `MSSQL_SA_PASSWORD` | — | SQL Server password |
| `DRIVER` | `{ODBC Driver 18 for SQL Server}` | ODBC driver name |
| `STOCK_PRICE_API_SYMBOL` | `IBM` | Stock symbol to fetch |
| `STOCK_PRICE_API_INTERVAL` | `5min` | API interval parameter |
| `STOCK_PRICE_API_FUNCTION` | `TIME_SERIES_DAILY` | API function parameter |
| `ALPHA_VANTAGE_API_KEY` | — | Alpha Vantage API key |

---

## Docker Commands

```bash
# Start MSSQL Server
docker compose -f docker/mssql.yaml up -d

# Stop MSSQL Server
docker compose -f docker/mssql.yaml down

# View logs
docker logs marketIntelligence_mssql-server

# Check container health
docker ps
```

---

## Testing

The project includes test scripts in the `tests/` directory:

| Test File | Description |
|-----------|-------------|
| `test_api_extract.py` | Validates API response extraction |
| `test_sql.py` | Tests MSSQL connectivity and database creation |
| `test_sql_path.py` | Verifies SQL file execution path resolution |
| `test_stock_price_api.py` | Tests the full stock price API integration |

> **Note:** Test files are standalone scripts. Run with `python tests/test_name.py`. For automated testing with pytest, consider migrating to `unittest` or `pytest` framework.

---

## Dependencies

- **pyodbc** — ODBC database connectivity for Python
- **pandas** — Data manipulation and transformation
- **requests** — HTTP client for Alpha Vantage API calls
- **python-dotenv** — Environment variable management

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) — Free stock market data API
- [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server) — Enterprise-grade database engine
- [pyodbc](https://github.com/mkleehammer/pyodbc) — Python ODBC connector
