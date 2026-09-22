import logging
import os
import pandas as pd
import numpy as np
from datetime import date
import unicodedata

logger = logging.getLogger(__name__)

CUSTOMERS = os.path.join("data/raw/customers_raw.csv")
TRANSACTIONS = os.path.join("data/raw/transactions_raw.csv")
DATA = os.path.join("data/")

def collect_data():
    pass
    return None

def normalise_texte(texte):
    if pd.isna(texte):
        return texte
    texte = texte.lower().strip() 
    texte = "".join(
            c for c in unicodedata.normalize('NFD', texte) 
            if unicodedata.category(c) != 'Mn'
    )   
    if texte in {'eur'}:
        return "EUR"
    if texte in {"cheque", "chèque"}:
        return 'CARTE_BANCAIRE'
    if texte in {"%liv%",'livre', 'livres'} :
        return "Livre"
    if texte in {"%tronique%", 'a‰lectronique',  'electroniqe', 'electronique'}:
        return "Electronique"
    if texte in {"%aison%", "maisons", "maison"}:
        return "Maison"
    if texte in {"%mode%","modes", "mode"}:
        return "Mode"
    if texte in {"%eaute%", "beaute"}:
        return "Beaute"
    if texte in {"%port%", "sports", "sport"}:
        return "Sport"
    if texte in {"%%"}:
        pass
    if texte in {"%tats-unis%","%states%", "us", "etats-unis","united states","etat-unis", "tats-unis"}:
        return "USA"
    if texte in {"be","belgique"}:
        return "Belgique"
    if texte in {"germany","allemagne","de"}:
        return "Allemagne"
    if texte in {"ch","suisse"}:
        return "Suisse"
    if texte in {"francia","fr","france"}:
        return "France"
    if texte in {'completed'}:
        return 'COMPLETED'
    if texte in {'bronze', 'argent'}:
        return 'BRONZE'
    return texte.upper().strip()

def clean_data():
    logger.info("Cleaning data...")
    df_transactions = pd.read_csv(TRANSACTIONS)
    df_customers = pd.read_csv(CUSTOMERS)

    logger.info("Cleaning Datetime ...")
    df_customers["birth_date"] = pd.to_datetime(df_customers['birth_date'], format="mixed", errors="coerce")
    df_customers['signup_date'] = pd.to_datetime(df_customers['signup_date'], format="mixed", errors="coerce")
    df_transactions["transaction_date"] = pd.to_datetime(df_transactions["transaction_date"], format="mixed", errors="coerce")

    logger.info("Drop doublons")
    df_transactions = df_transactions.drop_duplicates(subset=['transaction_id'], keep='first')
    df_customers = df_customers.drop_duplicates(subset=['customer_id'], keep='first')

    logger.info("Data cleaned columns")
    df_transactions['amount'] = df_transactions['amount'].astype(str).str.replace('$', '', regex=False).str.strip()
    df_transactions["amount"] = pd.to_numeric(df_transactions['amount'], errors='coerce')
    df_customers['phone'] = pd.to_numeric(df_customers['phone'], errors='coerce')
    df_customers['phone'] = df_customers['phone'].astype('Int64')
    mode_currency = df_transactions['currency'].mode()[0]
    df_transactions['currency'] = df_transactions['currency'].fillna(mode_currency)
    df_transactions['payment_method'] = df_transactions['payment_method'].apply(normalise_texte)
    df_transactions['status'] = df_transactions['status'].apply(normalise_texte)
    df_transactions['country'] = df_transactions['country'].apply(normalise_texte)
    df_transactions['currency'] = df_transactions['currency'].apply(normalise_texte)

    for col in df_transactions.columns:
        if df_transactions[col].isnull().any():
            df_transactions[col] = df_transactions[col].fillna(df_transactions[col].mode()[0])

    for col in df_customers.columns:
        if df_customers[col].isnull().any():
            df_customers[col] = df_customers[col].fillna(df_customers[col].mode()[0])

    logger.info("Cleaning data terminated ")
    return df_transactions, df_customers

def info_data():
    df_transactions = pd.read_csv(TRANSACTIONS)
    df_customers = pd.read_csv(CUSTOMERS)
    df_customers['country'] = df_customers['country'].apply(normalise_texte)
    return df_customers['country'].unique()


if __name__ == '__main__':
    transaction, customers = clean_data()
    logger.info("Data ingestion")
    transaction.to_parquet(os.path.join(DATA, "silver", "transactions.parquet"), index=False)
    customers.to_parquet(os.path.join(DATA, "silver", "customers.parquet"), index=False)
    logger.info("File parquet as save ")
    print(transaction.info())