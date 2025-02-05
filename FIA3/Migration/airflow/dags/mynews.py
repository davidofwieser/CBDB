import sqlite3
import requests
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# SQLite-Datenbankpfad
DB_PATH = "/opt/airflow/airflow.db"

# Funktionen zum Abrufen von Daten aus den öffentlichen APIs

def fetch_country_data():
    """Holt Daten zu einem Land (z. B. Deutschland)"""
    url = "https://restcountries.com/v3.1/name/germany"
    response = requests.get(url)
    data = response.json()[0]  # Erstes Land im Array
    country_name = data['name']['common']
    population = data['population']
    currency = list(data['currencies'].keys())[0]
    print(f"{country_name}: {population} Einwohner, Währung: {currency}")
    save_to_db("countries", {"country": country_name, "population": population, "currency": currency, "timestamp": datetime.now()})

def fetch_news_data():
    """Holt aktuelle Nachrichten-Schlagzeilen"""
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo"
    response = requests.get(url)
    data = response.json()
    if "articles" in data:
        headline = data["articles"][0]["title"]
        print(f"Neueste Nachricht: {headline}")
        save_to_db("news", {"headline": headline, "timestamp": datetime.now()})

def fetch_exchange_rate():
    """Holt den aktuellen Wechselkurs USD → EUR"""
    url = "https://v6.exchangerate-api.com/v6/91c658f8e62341de5b5a6275/latest/USD"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data["conversion_rates"]["EUR"]
    print(f"USD → EUR: {exchange_rate}")
    save_to_db("exchange_rates", {"usd_to_eur": exchange_rate, "timestamp": datetime.now()})

# Funktion zum Speichern der Daten in SQLite
def save_to_db(table_name, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Erstelle Tabelle, falls sie nicht existiert
    if table_name == "countries":
        cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            country TEXT,
                            population INTEGER,
                            currency TEXT,
                            timestamp TEXT)""")
    elif table_name == "news":
        cursor.execute("""CREATE TABLE IF NOT EXISTS news (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            headline TEXT,
                            timestamp TEXT)""")
    elif table_name == "exchange_rates":
        cursor.execute("""CREATE TABLE IF NOT EXISTS exchange_rates (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usd_to_eur REAL,
                            timestamp TEXT)""")

    # Daten einfügen
    cursor.execute(f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(['?']*len(data))})", tuple(data.values()))
    
    conn.commit()
    conn.close()
    print(f"✅ Daten in {table_name} gespeichert.")

# Airflow DAG-Definition
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 5),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "public_api_data_pipeline",
    default_args=default_args,
    schedule_interval=timedelta(minutes=30),  # Läuft alle 30 Minuten
    catchup=False
) as dag:

    task_countries = PythonOperator(
        task_id="fetch_country_data",
        python_callable=fetch_country_data
    )

    task_news = PythonOperator(
        task_id="fetch_news_data",
        python_callable=fetch_news_data
    )

    task_exchange = PythonOperator(
        task_id="fetch_exchange_rate",
        python_callable=fetch_exchange_rate
    )

    # Alle Tasks laufen parallel
    [task_countries, task_news, task_exchange]
