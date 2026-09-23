import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/features/leakage_dataset.parquet"


def evaluate(feature_name):
    df = pd.read_parquet(DATA_PATH)

    df = df.sort_values("transaction_date").copy()

    # On retire les lignes sans feature.
    df = df.dropna(subset=[feature_name])

    # Split temporel :
    # 80 % passé = entraînement
    # 20 % futur = test
    split_index = int(len(df) * 0.8)

    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

    X_train = train[[feature_name]]
    y_train = train["target"]

    X_test = test[[feature_name]]
    y_test = test["target"]

    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(),
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    auc = roc_auc_score(
        y_test,
        probabilities,
    )

    return accuracy, auc


if __name__ == "__main__":

    for feature in [
        "past_avg_7d",
        "future_avg_7d",
    ]:
        accuracy, auc = evaluate(feature)

        print()
        print(f"Feature : {feature}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"ROC-AUC : {auc:.4f}")