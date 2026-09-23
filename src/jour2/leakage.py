import pandas as pd


INPUT_PATH = "data/silver/transactions.parquet"
OUTPUT_PATH = "data/features/leakage_dataset.parquet"


def build_dataset():
    df = pd.read_parquet(INPUT_PATH)

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    df = df.sort_values(
        ["customer_id", "transaction_date"]
    ).copy()

    # ---------------------------------------------------------
    # TARGET
    # ---------------------------------------------------------
    median_amount = df["amount"].median()

    df["target"] = (
        df["amount"] > median_amount
    ).astype(int)

    # ---------------------------------------------------------
    # FEATURE CORRECTE :
    # uniquement les transactions des 7 jours précédents
    # ---------------------------------------------------------
    df["past_avg_7d"] = (
        df.groupby("customer_id")
        .rolling(
            "7D",
            on="transaction_date",
            closed="left",
        )["amount"]
        .mean()
        .reset_index(level=0, drop=True)
        .to_numpy()
    )

    # ---------------------------------------------------------
    # FEATURE AVEC LEAKAGE :
    # transactions futures dans les 7 jours suivants
    # ---------------------------------------------------------
    future_parts = []

    for customer_id, group in df.groupby("customer_id"):
        group = group.sort_values("transaction_date").copy()

        dates = group["transaction_date"]
        amounts = group["amount"]

        future_values = []

        for current_date in dates:
            mask = (
                (dates > current_date)
                & (dates <= current_date + pd.Timedelta(days=7))
            )

            if mask.any():
                future_values.append(amounts[mask].mean())
            else:
                future_values.append(float("nan"))

        group["future_avg_7d"] = future_values
        future_parts.append(group)

    df = pd.concat(future_parts, ignore_index=True)

    result = df[
        [
            "customer_id",
            "transaction_date",
            "amount",
            "past_avg_7d",
            "future_avg_7d",
            "target",
        ]
    ].copy()

    result.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    return result


if __name__ == "__main__":
    df = build_dataset()

    print(df.head(20).to_string(index=False))
    print()
    print("Nombre de lignes :", len(df))
    print()
    print("Valeurs manquantes :")
    print(df.isna().sum())