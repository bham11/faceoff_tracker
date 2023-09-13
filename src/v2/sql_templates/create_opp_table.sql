CREATE TABLE IF NOT EXISTS {{opponent}}
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        period INTEGER,
        player INTEGER,
        opponent INTEGER,
        strength TEXT,
        zone TEXT,
        result TEXT
    )