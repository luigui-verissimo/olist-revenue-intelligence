from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw_data"
    / "olist_orders_dataset.csv"
)


def load_orders_data() -> pd.DataFrame:
    """
    Load Olist orders dataset.
    
    Returns:
        pd.DataFrame: Loaded dataset
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    print(f"Dataset loaded successfully.")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nDataset Info:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nColumns:")
    print(df.columns.tolist())

    return df


if __name__ == "__main__":
    df = load_orders_data()
    print(df.head())