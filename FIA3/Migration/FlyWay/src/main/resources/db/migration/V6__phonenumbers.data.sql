INSERT INTO users (username, phone_number, email)
VALUES
    ('John Doe', '+431512345678', 'john.doe@example.com'),
    ('Jane Smith', '+431512345679', 'jane.smith@example.com'),
    ('Max Mustermann', '+431512345680', 'max.mustermann@example.com'),
    ('Lisa Müller', '+431512345681', 'lisa.mueller@example.com'),
    ('Tom Hanks', '+431512345682', 'tom.hanks@example.com'),
    ('Emma Watson', '+431512345683', 'emma.watson@example.com'),
    ('Chris Evans', '+431512345684', 'chris.evans@example.com'),
    ('Sophia Loren', '+431512345685', 'sophia.loren@example.com'),
    ('Leonardo DiCaprio', '+431512345686', 'leo.dicaprio@example.com'),
    ('Anne Hathaway', '+431512345687', 'anne.hathaway@example.com');
-- Füge weitere Einträge hinzu, falls mehr Daten benötigt werden
INSERT INTO users (username, phone_number, email)
SELECT
    'User' || x, -- Zufällige Namen
    '+43151' || MOD(x, 1000000), -- Zufällige Telefonnummern
    'user' || x || '@example.com' -- Zufällige E-Mails
FROM system_range(1, 100); -- Generiere 100 Benutzer