import sqlite3
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# SQLite Datenbank-Pfad
DB_PATH = "/opt/airflow/airflow.db"

# API Keys (falls nötig, sonst "" lassen)
OPENWEATHER_API_KEY = "dein_api_key"
GOOGLE_MAPS_API_KEY = "dein_api_key"
COFFEE_INDEX_API = "https://api.kaffee-preise.com/latest"

# Funktionen zur Datenextraktion
def extract_weather():
    """Extrahiert aktuelle Wetterdaten für eine Stadt."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Berlin&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    condition = data['weather'][0]['description']
    print(f"Wetter in Berlin: {temperature}°C, {condition}")
    save_to_db("weather", {"temperature": temperature, "condition": condition, "timestamp": datetime.now()})

def extract_foot_traffic():
    """Extrahiert Passantenfrequenz in der Nähe eines Cafés von Google Maps API."""
    location = "52.5200,13.4050"  # Berlin Zentrum
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=500&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    num_people = len(data.get("results", []))  # Anzahl der erkannten Orte als Proxy für Fußgängerverkehr
    print(f"Fußgängerverkehr in Berlin: {num_people} Orte erkannt")
    save_to_db("foot_traffic", {"num_people": num_people, "timestamp": datetime.now()})

def extract_coffee_price():
    """Extrahiert aktuellen Kaffee-Bohnen-Preisindex."""
    response = requests.get(COFFEE_INDEX_API)
    data = response.json()
    coffee_price = data['price']
    print(f"Aktueller Kaffee-Preis: {coffee_price} USD/kg")
    save_to_db("coffee_price", {"price": coffee_price, "timestamp": datetime.now()})

# Speichern der Daten in SQLite
def save_to_db(table_name, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabellenstruktur definieren
    if table_name == "weather":
        cursor.execute("""CREATE TABLE IF NOT EXISTS weather (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            temperature REAL,
                            condition TEXT,
                            timestamp TEXT)""")
    elif table_name == "foot_traffic":
        cursor.execute("""CREATE TABLE IF NOT EXISTS foot_traffic (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            num_people INTEGER,
                            timestamp TEXT)""")
    elif table_name == "coffee_price":
        cursor.execute("""CREATE TABLE IF NOT EXISTS coffee_price (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            price REAL,
                            timestamp TEXT)""")

    # Daten speichern
    cursor.execute(f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(['?']*len(data))})", tuple(data.values()))
    
    conn.commit()
    conn.close()
    print(f"✅ Daten in {table_name} gespeichert.")

# Airflow DAG Definition
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 5),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "coffee_market_analysis",
    default_args=default_args,
    schedule_interval=timedelta(minutes=15),  # Alle 15 Minuten
    catchup=False
) as dag:

    task_weather = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_weather
    )

    task_traffic = PythonOperator(
        task_id="extract_foot_traffic",
        python_callable=extract_foot_traffic
    )

    task_coffee_price = PythonOperator(
        task_id="extract_coffee_price",
        python_callable=extract_coffee_price
    )

    # Alle Tasks laufen parallel
    [task_weather, task_traffic, task_coffee_price]
 