from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_data"


def load_dataset(file_name: str) -> pd.DataFrame:
    file_path = RAW_DATA_PATH / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def build_revenue_base() -> pd.DataFrame:

    orders_df = load_dataset(
        "olist_orders_dataset.csv"
    )

    items_df = load_dataset(
    "olist_order_items_dataset.csv"
)

    items_df = (
        items_df
        .groupby("order_id", as_index=False)
        .agg({
            "price": "sum",
            "freight_value": "sum"
        })
    )

    payments_df = load_dataset(
    "olist_order_payments_dataset.csv"
)

    payments_df = (
        payments_df
        .groupby("order_id", as_index=False)
        .agg({
            "payment_value": "sum"
        })
    )

    merged_df = (
        orders_df
        .merge(
            items_df,
            on="order_id",
            how="left"
        )
        .merge(
            payments_df,
            on="order_id",
            how="left"
        )
    )

    print("Revenue base created successfully.")
    print(f"Rows: {merged_df.shape[0]}")
    print(f"Columns: {merged_df.shape[1]}")
    print("\nUnique Orders:")
    print(merged_df["order_id"].nunique())

    print("\nDuplicated Orders:")
    print(
        merged_df["order_id"].duplicated().sum()
)

    return merged_df

def build_marketplace_base() -> pd.DataFrame:

    orders_df = load_dataset(
        "olist_orders_dataset.csv"
    )

    items_df = load_dataset(
        "olist_order_items_dataset.csv"
    )

    payments_df = load_dataset(
        "olist_order_payments_dataset.csv"
    )

    products_df = load_dataset(
        "olist_products_dataset.csv"
    )

    payments_df = (
        payments_df
        .groupby("order_id", as_index=False)
        .agg({
            "payment_value": "sum"
        })
    )

    marketplace_df = (
        items_df
        .merge(
            orders_df,
            on="order_id",
            how="left"
        )
        .merge(
            payments_df,
            on="order_id",
            how="left"
        )
        .merge(
            products_df[
                [
                    "product_id",
                    "product_category_name"
                ]
            ],
            on="product_id",
            how="left"
        )
    )

    print("Marketplace base created successfully.")
    print(f"Rows: {marketplace_df.shape[0]}")
    print(f"Columns: {marketplace_df.shape[1]}")

    return marketplace_df


if __name__ == "__main__":
    df = build_revenue_base()
    print(df.head())