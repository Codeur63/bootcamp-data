import time
import pandas as pd

INPUT_PATH = 'data/silver/transactions.parquet'
OUTPUT_PATH = 'data/jour3/transcations_pandas.parquet'

def run():
    start = time.perf_counter()
    df = pd.read_parquet(INPUT_PATH)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df = df[(df['status'] == 'completed') & (df['amount']>0)].copy()
    df['amount_transaction'] = df['amount']
    df = df.sort_values('transaction_date')
    df.to_parquet(OUTPUT_PATH)

    elapsed = time.perf_counter() - start
    print(f"Temps pandas : {elapsed:.4f} secondes")

if __name__ == '__main__':
    run()