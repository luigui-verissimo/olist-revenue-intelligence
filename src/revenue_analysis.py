import pandas as pd

from src.data_ingestion import build_revenue_base 


def analyze_monthly_revenue():

    df = build_revenue_base()

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    df["month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
    )

    monthly_revenue = (
        df.groupby("month")["payment_value"]
        .sum()
        .sort_index()
    )
    

    best_month = monthly_revenue.idxmax()
    best_revenue = monthly_revenue.max()

    clean_revenue = monthly_revenue["2017-02":"2018-08"]
    growth = clean_revenue.pct_change() * 100
    average_growth = growth.mean()

    return clean_revenue


if __name__ == "__main__":
    analyze_monthly_revenue()
