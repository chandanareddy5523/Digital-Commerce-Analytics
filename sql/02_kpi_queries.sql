-- Net Revenue
SELECT SUM(net_revenue) AS net_revenue FROM fact_sales;

-- AOV
SELECT SUM(net_revenue) / NULLIF(COUNT(DISTINCT order_id),0) AS aov FROM fact_sales;

-- Revenue by region
SELECT region, SUM(net_revenue) AS revenue FROM fact_sales GROUP BY region ORDER BY revenue DESC;

-- Repeat purchase rate
WITH customer_orders AS (SELECT customer_id, COUNT(DISTINCT order_id) order_count FROM fact_sales GROUP BY customer_id)
SELECT AVG(CASE WHEN order_count > 1 THEN 1.0 ELSE 0.0 END) AS repeat_purchase_rate FROM customer_orders;

-- Conversion rate
SELECT SUM(conversions) * 1.0 / NULLIF(SUM(sessions),0) AS conversion_rate FROM fact_web_activity;

-- Campaign ROAS
SELECT c.campaign_id, c.campaign_name, c.spend, SUM(f.net_revenue) AS revenue,
       SUM(f.net_revenue) / NULLIF(c.spend,0) AS roas
FROM dim_campaign c LEFT JOIN fact_sales f ON c.campaign_id=f.campaign_id
GROUP BY c.campaign_id,c.campaign_name,c.spend ORDER BY roas DESC;
