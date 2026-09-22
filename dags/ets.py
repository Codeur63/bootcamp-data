import os
import logging 
import pandas as pd
import great_expectations as ge
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from jour1.collect_data import clean_data
from jour1.validate_data import run_validation

logger = logging.getLogger(__name__)

default_args = {
    "owner": 'data_team',
    'depends_on_past': False,
    'start_date':datetime(2026,7,22),
    'email_on_failure':False,
    'retries':3,
    'retry_delay':timedelta(minutes=5),
    'execution_timeout':timedelta(hours=2)
}

DATA = os.path.join("data/")

with DAG(
    'pipeline_etl',
    default_args = default_args,
    description = 'Pipeline ETl avec validation de contrat de donnees Great Expectations',
    schedule = None,
    catchup=False,
    tags=["Team1", "ETL", "Validate data"]    
) as dag:
    task_ingestion = PythonOperator(task_id='ingestion_csv', python_callable=clean_data)
   
    task_validation = PythonOperator(
       task_id='Validation_grat_expectations',
       python_callable = run_validation
    ) 

    task_ingestion >> task_validation