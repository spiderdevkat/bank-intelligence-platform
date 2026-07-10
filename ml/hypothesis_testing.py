import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from scipy import stats

from db.postgres_client import get_connection


def load_transactions_df():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM fact_transactions", conn)
    conn.close()
    return df

def chi_square_fraud_vs_channel(df):
    contingency_table = pd.crosstab(df["channel"], df["is_fraud"])
    print("\nContingency table:")
    print(contingency_table)

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    print(f"\nchi2 statistic: {chi2:.4f}")
    print(f"p-value: {p_value:.10f}")
    print(f"degrees of freedom: {dof}")
    return chi2, p_value

if __name__ == "__main__":
    df = load_transactions_df()
    print(f"Total transactions: {len(df)}")
    print(f"Fraud transactions: {df['is_fraud'].sum()}")

    fraud_amounts = df[df["is_fraud"]]["amount"]
    normal_amounts = df[~df["is_fraud"]]["amount"]

    print(f"\nFraud mean amount:  {fraud_amounts.mean():.2f}")
    print(f"Normal mean amount: {normal_amounts.mean():.2f}")

    chi_square_fraud_vs_channel(df)

    t_stat, p_value = stats.ttest_ind(fraud_amounts, normal_amounts, equal_var=False)
    print(f"\nt-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.10f}")