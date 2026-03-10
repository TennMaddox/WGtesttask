import sqlite3
from pathlib import Path

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS weapons (
    weapon TEXT PRIMARY KEY,
    reload_speed INTEGER,
    rotational_speed INTEGER,
    diameter INTEGER,
    power_volley INTEGER,
    count INTEGER
);

CREATE TABLE IF NOT EXISTS hulls (
    hull TEXT PRIMARY KEY,
    armor INTEGER,
    type INTEGER,
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS engines (
    engine TEXT PRIMARY KEY,
    power INTEGER,
    type INTEGER
);

CREATE TABLE IF NOT EXISTS ships (
    ship TEXT PRIMARY KEY,
    weapon TEXT,
    hull TEXT,
    engine TEXT,
    FOREIGN KEY (weapon) REFERENCES weapons(weapon),
    FOREIGN KEY (hull) REFERENCES hulls(hull),
    FOREIGN KEY (engine) REFERENCES engines(engine)
);
"""


def create_schema(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(CREATE_TABLES_SQL)
        conn.commit()
    finally:
        conn.close()
