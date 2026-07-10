import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from db.postgres_client import get_connection


def load_transactions_df():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM fact_transactions", conn)
    conn.close()
    return df


def build_features(df):
    features = df[["amount"]].copy()

    features["hour_of_day"] = pd.to_datetime(df["transaction_timestamp"]).dt.hour
    features["day_of_week"] = pd.to_datetime(df["transaction_timestamp"]).dt.dayofweek

    channel_dummies = pd.get_dummies(df["channel"], prefix="channel")
    type_dummies = pd.get_dummies(df["transaction_type"], prefix="type")

    features = pd.concat([features, channel_dummies, type_dummies], axis=1)
    labels = df["is_fraud"]

    return features, labels


if __name__ == "__main__":
    df = load_transactions_df()
    features, labels = build_features(df)
    print(f"Feature columns: {list(features.columns)}")
    print(f"Feature matrix shape: {features.shape}")
    print(features.head(3))