import pandas as pd
import numpy as np
from pathlib import Path
from .config import RAW, PROCESSED
from .validation import validate_file
from .logger import get_logger

log = get_logger(__name__)

def clean_data() -> dict[str, pd.DataFrame]:
    dfs = {name: validate_file(RAW / name) for name in ["customers.csv", "products.csv", "orders.csv", "web_sessions.csv", "campaigns.csv"]}
    customers, products, orders, web, campaigns = dfs.values()

    customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce")
    products["unit_price"] = pd.to_numeric(products["unit_price"], errors="coerce").fillna(0)
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    web["session_date"] = pd.to_datetime(web["session_date"], errors="coerce")
    campaigns["spend"] = pd.to_numeric(campaigns["spend"], errors="coerce").fillna(0)

    for c in ["quantity", "unit_price", "discount_pct"]:
        orders[c] = pd.to_numeric(orders[c], errors="coerce").fillna(0)
    orders["quantity"] = orders["quantity"].clip(lower=0)
    orders["discount_pct"] = orders["discount_pct"].clip(0, 100)
    orders = orders.drop_duplicates(subset=["order_id", "product_id"])
    orders["gross_amount"] = orders["quantity"] * orders["unit_price"]
    orders["discount_amount"] = orders["gross_amount"] * orders["discount_pct"] / 100
    orders["net_amount"] = orders["gross_amount"] - orders["discount_amount"]
    orders["is_return"] = orders["status"].isin(["Returned", "Refunded"])
    orders["net_revenue"] = np.where(orders["is_return"], -orders["net_amount"], orders["net_amount"])

    # Standardize text dimensions.
    for df, cols in [(customers, ["region"]), (products, ["category"]), (orders, ["status", "channel", "region"]), (web, ["channel"])]:
        for c in cols:
            df[c] = df[c].astype(str).str.strip().str.title()

    dim_customer = customers.copy()
    dim_product = products.copy()
    dim_campaign = campaigns.copy()
    dim_date = pd.DataFrame({"date": pd.date_range(orders["order_date"].min(), orders["order_date"].max(), freq="D")})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)

    fact_sales = orders[["order_id","order_date","customer_id","product_id","campaign_id","channel","region","quantity","unit_price","discount_pct","gross_amount","discount_amount","net_revenue","status","is_return"]].copy()
    fact_web = web.copy()

    result = {"dim_customer": dim_customer, "dim_product": dim_product, "dim_campaign": dim_campaign, "dim_date": dim_date, "fact_sales": fact_sales, "fact_web_activity": fact_web}
    for name, df in result.items():
        df.to_csv(PROCESSED / f"{name}.csv", index=False)
    log.info("Processed %s rows across analytical datasets", len(fact_sales))
    return result
