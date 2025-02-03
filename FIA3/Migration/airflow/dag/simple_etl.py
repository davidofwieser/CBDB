from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

import requests

import json

import sqlite3
 


# Standard Airflow DAG-Argumente

default_args = {

    'owner': 'airflow',

    'depends_on_past': False,

    'start_date': datetime(2024, 1, 1),

    'retries': 1,

    'retry_delay': timedelta(minutes=5),

}



# Definiere den DAG

dag = DAG(

    'simple_etl_pipeline',

    default_args=default_args,

    description='Ein einfacher ETL-Prozess mit Airflow',

    schedule_interval='@daily',  # Täglich ausführen

)



# Extract - Daten aus einer API abrufen

def extract():

    url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    response = requests.get(url)

    data = response.json()

    with open('/tmp/extracted_data.json', 'w') as f:

        json.dump(data, f)

    print("Daten extrahiert!")



# Transform - Daten umwandeln

def transform():

    with open('/tmp/extracted_data.json', 'r') as f:

        data = json.load(f)

    transformed_data = {

        'time': data['time']['updated'],

        'USD_rate': data['bpi']['USD']['rate_float'],

    }

    with open('/tmp/transformed_data.json', 'w') as f:

        json.dump(transformed_data, f)

    print("Daten transformiert!")



# Load - Daten in eine SQLite-Datenbank speichern

def load():

    with open('/tmp/transformed_data.json', 'r') as f:

        data = json.load(f)

    conn = sqlite3.connect('/tmp/airflow_etl.db')

    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS bitcoin_prices (

            time TEXT,

            USD_rate REAL

        )

    ''')

    cursor.execute('''

        INSERT INTO bitcoin_prices (time, USD_rate) VALUES (?, ?)

    ''', (data['time'], data['USD_rate']))

    conn.commit()

    conn.close()

    print("Daten geladen!")



# Airflow Tasks definieren

extract_task = PythonOperator(

    task_id='extract',

    python_callable=extract,

    dag=dag,

)



transform_task = PythonOperator(

    task_id='transform',

    python_callable=transform,

    dag=dag,

)



load_task = PythonOperator(

    task_id='load',

    python_callable=load,

    dag=dag,

)



# Task-Abhängigkeiten definieren

extract_task >> transform_task >> load_task

