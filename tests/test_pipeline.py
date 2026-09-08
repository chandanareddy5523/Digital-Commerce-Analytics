from pathlib import Path
import pandas as pd
from src.validation import validate_file
from src.config import RAW

def test_raw_files_exist():
    for name in ["customers.csv", "products.csv", "orders.csv", "web_sessions.csv", "campaigns.csv"]:
        assert (RAW / name).exists()

def test_orders_have_positive_ids():
    df = pd.read_csv(RAW / "orders.csv")
    assert df["order_id"].notna().all()
    assert (df["quantity"] >= 0).all()
