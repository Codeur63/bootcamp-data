import time
import polars as pl

INPUT_PATH = 'data/silver/transactions.parquet'
OUTPUT_PATH = 'data/jour3/transactions_polars.parquet'

def run():
    start = time.perf_counter()    
    df = pl.read_parquet(INPUT_PATH)
    df = (
        df.with_columns(
           pl.col('transaction_date').cast(pl.Datetime)
        ).filter(
            (pl.col('status').eq('completed')) 
            & (pl.col('amount').gt(0))
        ).with_columns(
            pl.col('amount').alias('amount_transaction')
        ).sort('transaction_date')
    )
    
    df.write_parquet(OUTPUT_PATH)

    elapsed = time.perf_counter() - start
    print(f"Temps pandas : {elapsed:.4f} secondes")

if __name__ == '__main__':
    run()
