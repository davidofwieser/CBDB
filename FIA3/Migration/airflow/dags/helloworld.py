from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
	

def my_python_task():
    print("Hello, Airflow!")

# DAG-Definition
with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2024, 2, 5),
    schedule_interval=timedelta(seconds=30), 
    catchup=False
) as dag:

    start = DummyOperator(task_id="start")

    task1 = PythonOperator(
        task_id="print_hello",
        python_callable=my_python_task
    )

    end = DummyOperator(task_id="end")

    # Task-Abhängigkeiten definieren
    start >> task1 >> end  # Reihenfolge: start -> task1 -> end

