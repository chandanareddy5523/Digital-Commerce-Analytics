from pathlib import Path
import pandas as pd

REQUIRED = {
    "customers.csv": ["customer_id", "customer_name", "region", "signup_date"],
    "products.csv": ["product_id", "product_name", "category", "unit_price"],
    "orders.csv": ["order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price", "discount_pct", "status", "channel", "region", "campaign_id"],
    "web_sessions.csv": ["session_id", "session_date", "customer_id", "channel", "sessions", "conversions"],
    "campaigns.csv": ["campaign_id", "campaign_name", "spend"],
}

def validate_file(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    required = REQUIRED[path.name]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{path.name}: missing columns {missing}")
    if df.empty:
        raise ValueError(f"{path.name}: file is empty")
    return df
