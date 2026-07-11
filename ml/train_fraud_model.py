import sys
from pathlib import Path
import joblib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from ml.features import load_transactions_df, build_features

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

import pandas as pd

def train_knn(X_train, X_test, y_train, y_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print("\n--- KNN Classification report ---")
    print(classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier


def train_random_forest(X_train, X_test, y_train, y_test, feature_names):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n--- Random Forest Classification report ---")
    print(classification_report(y_test, y_pred))

    importances = pd.Series(model.feature_importances_, index=feature_names)
    print("\nTop 5 most important features:")
    print(importances.sort_values(ascending=False).head(5))

    return model

if __name__ == "__main__":
    df = load_transactions_df()
    features, labels = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"Fraud rate in train: {y_train.mean():.2%}")
    print(f"Fraud rate in test: {y_test.mean():.2%}")

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    train_knn(X_train, X_test, y_train, y_test)

    rf_model = train_random_forest(X_train, X_test, y_train, y_test, features.columns)

    Path("ml/models").mkdir(parents=True, exist_ok=True)
    joblib.dump(rf_model, "ml/models/fraud_random_forest.joblib")
    print("\nModel saved to ml/models/fraud_random_forest.joblib")