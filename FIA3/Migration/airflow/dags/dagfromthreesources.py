from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def extract_from_source_1():
    print("Daten von Quelle 1 extrahieren")

def extract_from_source_2():
    print("Daten von Quelle 2 extrahieren")

def extract_from_source_3():
    print("Daten von Quelle 3 extrahieren")

def process_data():
    print("Daten zusammenführen und verarbeiten")

with DAG(
    dag_id="multi_source_dag",
    start_date=datetime(2024, 2, 5),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    task_1 = PythonOperator(
        task_id="extract_source_1",
        python_callable=extract_from_source_1
    )

    task_2 = PythonOperator(
        task_id="extract_source_2",
        python_callable=extract_from_source_2
    )

    task_3 = PythonOperator(
        task_id="extract_source_3",
        python_callable=extract_from_source_3
    )

    process = PythonOperator(
        task_id="process_data",
        python_callable=process_data
    )

    # Die drei Extraktions-Tasks laufen parallel und dann wird verarbeitet
    [task_1, task_2, task_3] >> process
