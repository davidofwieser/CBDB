ALTER TABLE users ADD phone_number INTEGER;


INSERT INTO users (username, phone_number, email)
VALUES
    ('asdf', 15123, 'john.doe@example.com'),
    ('qwert', 1512345, 'jane.smith@example.com');