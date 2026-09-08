# Digital Commerce Customer & Revenue Intelligence

Enterprise-style Data Analyst portfolio project aligned with Chandana's resume.

## Project objective
Build a repeatable analytics pipeline for e-commerce orders, customers, products, campaigns and web sessions. The pipeline validates raw CSV data, cleans and enriches it, calculates business KPIs, creates an analytical star-schema dataset, exports Excel reports, and produces dashboard-ready CSVs for Power BI/Tableau.

## Business KPIs
- Gross Revenue
- Net Revenue
- Average Order Value (AOV)
- Conversion Rate
- Repeat Purchase Rate
- Return Rate
- Customer Lifetime Value proxy
- Marketing ROAS
- Revenue by Product, Region, Channel and Campaign

## Technology
Python 3.13+, pandas, NumPy, Matplotlib, Seaborn, openpyxl, SQL, Power BI/Tableau.

## Folder structure
```
chandana_digital_commerce_project/
├── config/settings.json
├── data/raw/*.csv
├── data/processed/
├── logs/
├── reports/
├── sql/01_schema.sql
├── sql/02_kpi_queries.sql
├── src/
│   ├── config.py
│   ├── logger.py
│   ├── validation.py
│   ├── pipeline.py
│   ├── analysis.py
│   └── main.py
├── tests/test_pipeline.py
├── requirements.txt
└── README.md
```

## How to run on Windows
1. Install Python 3.13+.
2. Open Command Prompt in this project folder.
3. Create environment: `py -3.13 -m venv .venv`
4. Activate: `.venv\\Scripts\\activate`
5. Install: `python -m pip install --upgrade pip` then `pip install -r requirements.txt`
6. Run: `python -m src.main`
7. Open the generated files under `data/processed/` and `reports/`.
8. Run tests: `python -m pytest`

No database is required for the default run. The SQL folder contains production-style SQL examples for loading the same analytical model into SQL Server/PostgreSQL/Snowflake.

## Power BI
Use Get Data > Text/CSV and load the generated `fact_sales.csv`, `fact_web_activity.csv`, and dimension CSVs from `data/processed/`. Create one-to-many relationships from dimensions to facts. Use `dim_date` as the date table. Suggested report pages: Executive Overview, Sales & Product, Customer, Marketing, Returns.

## Important
The sample data is synthetic and created only for portfolio/demo purposes. Replace files in `data/raw/` with approved business data without changing the pipeline interface.
