import sqlite3

from app.models.Hull import Hull


class HullRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_by_name(self, name: str) -> Hull:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT hull, armor, type, capacity FROM hulls WHERE hull = ?",
            (name,),
        )
        row = cur.fetchone()
        return Hull(*row)