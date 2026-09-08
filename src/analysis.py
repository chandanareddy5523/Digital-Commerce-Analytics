import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .config import PROCESSED, REPORTS
from .logger import get_logger

log = get_logger(__name__)

def build_report() -> None:
    sales = pd.read_csv(PROCESSED / "fact_sales.csv", parse_dates=["order_date"])
    web = pd.read_csv(PROCESSED / "fact_web_activity.csv", parse_dates=["session_date"])
    campaigns = pd.read_csv(PROCESSED / "dim_campaign.csv")

    total_orders = sales["order_id"].nunique()
    gross = sales["gross_amount"].sum()
    net = sales["net_revenue"].sum()
    aov = net / total_orders if total_orders else 0
    returned = sales.loc[sales["is_return"], "order_id"].nunique()
    return_rate = returned / total_orders if total_orders else 0
    customers = sales.groupby("customer_id")["order_id"].nunique()
    repeat_rate = (customers.gt(1).sum() / len(customers)) if len(customers) else 0
    sessions = web["sessions"].sum()
    conversions = web["conversions"].sum()
    conversion_rate = conversions / sessions if sessions else 0
    campaign_revenue = sales.groupby("campaign_id")["net_revenue"].sum().reset_index(name="revenue")
    campaign_kpi = campaigns.merge(campaign_revenue, on="campaign_id", how="left").fillna({"revenue":0})
    campaign_kpi["roas"] = campaign_kpi["revenue"] / campaign_kpi["spend"].replace(0, pd.NA)

    kpis = pd.DataFrame({"KPI":["Gross Revenue","Net Revenue","AOV","Return Rate","Repeat Purchase Rate","Conversion Rate"],"Value":[gross,net,aov,return_rate,repeat_rate,conversion_rate]})
    by_region = sales.groupby("region", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
    by_category = sales.merge(pd.read_csv(PROCESSED / "dim_product.csv"), on="product_id").groupby("category", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
    with pd.ExcelWriter(REPORTS / "digital_commerce_kpi_report.xlsx", engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="KPI Summary", index=False)
        by_region.to_excel(writer, sheet_name="Revenue by Region", index=False)
        by_category.to_excel(writer, sheet_name="Revenue by Category", index=False)
        campaign_kpi.to_excel(writer, sheet_name="Campaign ROAS", index=False)
        sales.to_excel(writer, sheet_name="Fact Sales", index=False)
    # Charts
    plt.figure(figsize=(8,5)); sns.barplot(data=by_region, x="region", y="net_revenue"); plt.title("Net Revenue by Region"); plt.xticks(rotation=30); plt.tight_layout(); plt.savefig(REPORTS / "revenue_by_region.png", dpi=150); plt.close()
    plt.figure(figsize=(8,5)); sns.barplot(data=by_category, x="category", y="net_revenue"); plt.title("Net Revenue by Category"); plt.xticks(rotation=30); plt.tight_layout(); plt.savefig(REPORTS / "revenue_by_category.png", dpi=150); plt.close()
    log.info("Report generated")
