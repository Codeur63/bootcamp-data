import os
import pandas as pd
import great_expectations as ge
import logging

logger = logging.getLogger(__name__)

TRANSACTION = os.path.join("data/silver/transactions.parquet")
CUSTOMERS = os.path.join("data/silver/customers.parquet")

def run_validation():
    logger.info("Validate quality of data ")

    context = ge.get_context(mode="ephemeral")
    
    ge_df_transaction = context.sources.pandas_defaultread_parquet(TRANSACTION)
    ge_df_customers = context.sources.pandas_default.read_parquet(CUSTOMERS)
    
    ckeck_id_transaction = ge_df_transaction.expect_column_values_to_be_unique('transaction_id')
    check_country = ge_df_transaction.expect_column_values_to_be_unique('country')
    
    check_country_customers = ge_df_customers.expect_column_values_to_be_unique('country')
    check_id_customers = ge_df_customers.expect_column_values_to_be_unique('customer_id')
    check_email_customers = ge_df_customers.expect_column_values_to_not_be_null(column='email')
    check_name_customer = ge_df_customers.expect_column_values_to_not_be_null(column='full_name')
    check_amount_transaction = ge_df_transaction.expect_column_values_to_not_be_null(column='amount')
    check_date_transaction = ge_df_transaction.expect_column_values_to_not_be_null(column='transaction_date')
    
    errors = []
    
    if not ckeck_id_transaction.success:
        errors.append(ckeck_id_transaction)
        logger.error("check_id_transaction failed")
    if not check_id_customers.success:
        errors.append(check_id_customers)
        logger.error("check_id_customers failed")
    if not check_email_customers.success:
        errors.append(check_email_customers)
        logger.error("check_email_customers failed")
    if not check_name_customer.success:
        errors.append(check_name_customer)
        logger.error("check_name_customer failed")
    if not check_amount_transaction.success:
        errors.append(check_amount_transaction)
        logger.error("check_amount_transaction failed")
    if not check_date_transaction.success:
        errors.append(check_date_transaction)
        logger.error("check_date_transaction failed")

    return True    
