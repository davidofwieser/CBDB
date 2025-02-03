import json
import time
from pymongo import MongoClient

# Verbindung zu MongoDB
mongo_client = MongoClient("mongodb://admin:geheimespasswort@localhost:27017/")
db = mongo_client["maxwell_db"]
collection = db["mysql_changes"]

# Pfad zur Maxwell-Ausgabedatei
file_path = "C:/Users/David/maxwell_data/output.json"

def import_maxwell_data():
    print("📌 Übertrage Maxwell-Daten nach MongoDB...")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    data = json.loads(line.strip())  # JSON-Zeile einlesen
                    collection.insert_one(data)     # In MongoDB speichern
                    print(f"✅ Eingefügt: {data}")
                except json.JSONDecodeError as e:
                    print(f"⚠ Fehler beim Parsen: {e}")
    except FileNotFoundError:
        print(f"🚨 Datei nicht gefunden: {file_path}")
    
    print("✅ Alle Daten wurden übertragen!")

# Skript alle 10 Sekunden ausführen (optional für Live-Import)
while True:
    import_maxwell_data()
    print("⏳ Warte 10 Sekunden...")
    time.sleep(10)
