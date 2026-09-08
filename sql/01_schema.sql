-- PostgreSQL/Snowflake-style analytical model. Adapt data types for SQL Server if required.
CREATE TABLE dim_customer (customer_id VARCHAR(20) PRIMARY KEY, customer_name VARCHAR(100), region VARCHAR(50), signup_date DATE);
CREATE TABLE dim_product (product_id VARCHAR(20) PRIMARY KEY, product_name VARCHAR(150), category VARCHAR(80), unit_price DECIMAL(18,2));
CREATE TABLE dim_campaign (campaign_id VARCHAR(20) PRIMARY KEY, campaign_name VARCHAR(150), spend DECIMAL(18,2));
CREATE TABLE dim_date (date DATE PRIMARY KEY, year INT, month INT, month_name VARCHAR(20), quarter VARCHAR(5));
CREATE TABLE fact_sales (order_id VARCHAR(20), order_date DATE, customer_id VARCHAR(20), product_id VARCHAR(20), campaign_id VARCHAR(20), channel VARCHAR(50), region VARCHAR(50), quantity INT, unit_price DECIMAL(18,2), discount_pct DECIMAL(5,2), gross_amount DECIMAL(18,2), discount_amount DECIMAL(18,2), net_revenue DECIMAL(18,2), status VARCHAR(30), is_return BOOLEAN);
CREATE TABLE fact_web_activity (session_id VARCHAR(20), session_date DATE, customer_id VARCHAR(20), channel VARCHAR(50), sessions INT, conversions INT);
