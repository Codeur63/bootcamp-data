import pandas as pd 


def build_features() -> pd.DataFrame:
    transaction = pd.read_parquet("../../data/silver/transactions.parquet")
    transaction = transaction.sort_values(['customer_id', 'transaction_date'])

    features_rows = []

    for customer_id, group in transaction.groupby("customer_id"):
       group = group.sort_values("transaction_date").copy()
       group["avg_amount_7d"] = (
                   group
                   .set_index("transaction_date")["amount"]
                   .rolling("7D", closed="left")
                   .mean()
                   .to_numpy()
               )
       features_rows.append(group[['customer_id', 'transaction_date', 'avg_amount_7d']])

    features = pd.concat(features_rows, ignore_index=True)
    features.to_parquet("../../data/features/transactions_features.parquet", index=False)
    return features

def build_transaction() -> pd.DataFrame:    
    transaction = pd.read_parquet("../data/silver/transactions.parquet")
    transaction = transaction[transaction['status'] == 'COMPLETED'].copy()
    transaction = transaction.sort_values(['customer_id', 'transaction_date'])

    transaction['avg_amount_7d'] = (
        transaction.set_index('transaction_date').groupby('customer_id')['amount'].rolling('7D').mean().reset_index(level=0, drop=True).values
    )

    features = transaction[['customer_id', 'transaction_date', 'avg_amount_7d']].copy()

    features.to_parquet("../data/features/transactions.parquet")

    return features


if __name__ == "__main__":
    features = build_features()
    print(features.head())
    print(f"Features shape: {features.shape}")
    
    