import sqlite3
from typing import List

from app.models.Ship import Ship

class ShipRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all_ships(self) -> List[Ship]:
        cur = self._conn.cursor()
        cur.execute("SELECT ship, weapon, hull, engine FROM ships ORDER BY ship")
        rows = cur.fetchall()
        return [Ship(*row) for row in rows]