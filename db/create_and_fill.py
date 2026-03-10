import random
import sqlite3
from pathlib import Path

from .schema import create_schema

#Ограничения для INT по условию задания
INT_MIN, INT_MAX = 1, 20

#Вспомогательная функция, чтобы не вызывать каждый раз random.randint с константами
def _rand() -> int:
    return random.randint(INT_MIN, INT_MAX)


def create_and_fill(db_path: Path) -> None:
    create_schema(db_path)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()

        # weapons: 20
        for i in range(1, 21):
            cur.execute(
                "INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)",
                (f"weapon-{i}", _rand(), _rand(), _rand(), _rand(), _rand()),
            )

        # hulls: 5
        for i in range(1, 6):
            cur.execute(
                "INSERT INTO hulls VALUES (?, ?, ?, ?)",
                (f"hull-{i}", _rand(), _rand(), _rand()),
            )

        # engines: 6
        for i in range(1, 7):
            cur.execute(
                "INSERT INTO engines VALUES (?, ?, ?)",
                (f"engine-{i}", _rand(), _rand()),
            )

        # ships: 200
        for i in range(1, 201):
            cur.execute(
                "INSERT INTO ships VALUES (?, ?, ?, ?)",
                (
                    f"ship-{i}",
                    f"weapon-{random.randint(1, 20)}",
                    f"hull-{random.randint(1, 5)}",
                    f"engine-{random.randint(1, 6)}",
                ),
            )

        conn.commit()
    finally:
        conn.close()
