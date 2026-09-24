from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_PATH = "data/silver/transactions.parquet"

TRAIN_PATH = "data/jour3/split/train.parquet"
TEST_PATH = "data/jour3/split/test.parquet"

SEED = 42
TEST_SIZE = 0.2

def split_dataset(input_path: Path):
    df = pd.read_parquet(input_path)
    df['target'] = (df['status'] == 'COMPLETED').astype(int)
    train, test = train_test_split(df, test_size=TEST_SIZE, random_state=42, stratify=df['target']) 

    train.to_parquet(TRAIN_PATH)
    test.to_parquet(TEST_PATH)
    print(f"Train: {len(train)}, Test: {len(test)}")
    
if __name__ == "__main__":
    split_dataset(INPUT_PATH)

