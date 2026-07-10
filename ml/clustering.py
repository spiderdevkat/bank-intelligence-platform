import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from db.postgres_client import get_connection


def load_customer_features():
    conn = get_connection()
    query = """
        SELECT
            customer_id,
            COUNT(*) AS transaction_count,
            SUM(amount) AS total_volume,
            AVG(amount) AS avg_amount,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_count
        FROM fact_transactions
        GROUP BY customer_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def find_elbow(features_scaled, max_k=8):
    inertias = []
    for k in range(1, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(features_scaled)
        inertias.append(model.inertia_)
        print(f"K={k}: inertia={model.inertia_:.2f}")
    return inertias

def fit_without_fraud_signal(df, k=4):
    """Re-cluster using ONLY behavioral features, no fraud_count at all —
    to test whether risky customers separate out on their own, or whether
    the earlier clustering only worked because we fed it the answer."""
    feature_cols_no_fraud = ["transaction_count", "total_volume", "avg_amount"]
    X = df[feature_cols_no_fraud]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster_no_fraud_signal"] = model.fit_predict(X_scaled)

    print(f"\n--- Cluster profiles WITHOUT fraud_count as input (K={k}) ---")
    print(df.groupby("cluster_no_fraud_signal")[feature_cols_no_fraud + ["fraud_count"]].mean())
    print("\nCluster sizes:")
    print(df["cluster_no_fraud_signal"].value_counts().sort_index())

    return df

if __name__ == "__main__":
    df = load_customer_features()
    print(f"Customers with at least 1 transaction: {len(df)}")
    print(df.describe())

    feature_cols = ["transaction_count", "total_volume", "avg_amount", "fraud_count"]
    X = df[feature_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("\n--- Elbow method ---")
    find_elbow(X_scaled)

    df = fit_without_fraud_signal(df, k=4)