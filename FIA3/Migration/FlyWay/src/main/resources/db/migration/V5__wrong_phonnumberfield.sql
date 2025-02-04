-- Schritt 1: Neue Spalte mit dem richtigen Datentyp erstellen
ALTER TABLE users ADD phone_number_temp VARCHAR(20);

-- Schritt 2: Daten von der alten Spalte in die neue Spalte übertragen
UPDATE users SET phone_number_temp = CAST(phone_number AS VARCHAR);

-- Schritt 3: Alte Spalte entfernen
ALTER TABLE users DROP COLUMN phone_number;

-- Schritt 4: Neue Spalte umbenennen
ALTER TABLE users RENAME COLUMN phone_number_temp TO phone_number;