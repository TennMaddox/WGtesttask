import sqlite3

from app.models.Weapon import Weapon


class WeaponRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_by_name(self, name: str) -> Weapon:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT weapon, reload_speed, rotational_speed, diameter, power_volley, count "
            "FROM weapons WHERE weapon = ?",
            (name,),
        )
        row = cur.fetchone()
        return Weapon(*row)