import sqlite3

from app.models.Engine import Engine

class EngineRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_by_name(self, name: str) -> Engine:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT engine, power, type FROM engines WHERE engine = ?",
            (name,),
        )
        row = cur.fetchone()
        return Engine(*row)