import random
import shutil
import sqlite3
from pathlib import Path

from .create_and_fill import INT_MIN, INT_MAX


class DatabaseRandomizer:
    def __init__(self, src: Path, dst: Path):
        self._src = src
        self._dst = dst

    def create_randomized_copy(self) -> None:
        print(f"[DB] Copying DB from {self._src} to {self._dst}")
        shutil.copy(self._src, self._dst)
        conn = sqlite3.connect(self._dst)
        try:
            self._randomize(conn)
            conn.commit()
        finally:
            conn.close()

    def _rand_param(self) -> int:
        return random.randint(INT_MIN, INT_MAX)

    # ---------------------------------------------------------
    # Получение всехкораблей и списков компонентов
    # ---------------------------------------------------------
    def _get_component_list_from_table(self, conn, table, column):
        cur = conn.cursor()
        cur.execute(f"SELECT {column} FROM {table}")
        return [row[0] for row in cur.fetchall()]

    def _get_ships_from_table(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT ship, weapon, hull, engine FROM ships")
        return cur.fetchall()

    def _load_data(self, conn):
        ships = self._get_ships_from_table(conn)
        all_weapons = self._get_component_list_from_table(conn, "weapons", "weapon")
        all_hulls = self._get_component_list_from_table(conn, "hulls", "hull")
        all_engines = self._get_component_list_from_table(conn, "engines", "engine")
        return ships, all_weapons, all_hulls, all_engines

    # ---------------------------------------------------------
    # Вспомогательный метод по обновлению компонента
    # ---------------------------------------------------------
    def _update_ship_component(self, conn, ship, component_name, new_value):
        print(f"[SHIP] {ship}: change {component_name} -> {new_value}")
        conn.execute(
            f"UPDATE ships SET {component_name} = ? WHERE ship = ?",
            (new_value, ship)
        )

    # ---------------------------------------------------------
    # Вспомогательный метод по обновлению одного параметра (но если не был изменен ранее)
    # ---------------------------------------------------------
    def _update_component_param_once(self, conn, component_value,
                                     changed_set, table, key_column, fields):

        if component_value in changed_set:
            print(f"[SKIP] {table[:-1]} '{component_value}' already changed before, skip params")
            return  # уже меняли — больше не трогаем

        field = random.choice(fields)
        new_val = self._rand_param()

        # Лог до изменения
        cur = conn.cursor()
        cur.execute(
            f"SELECT {field} FROM {table} WHERE {key_column} = ?",
            (component_value,)
        )
        row = cur.fetchone()
        old_val = row[0] if row is not None else None

        print(
            f"[CHANGE] {table[:-1]} '{component_value}': "
            f"{field} {old_val} -> {new_val}"
        )

        conn.execute(
            f"UPDATE {table} SET {field} = ? WHERE {key_column} = ?",
            (new_val, component_value),
        )
        changed_set.add(component_value)

    # ---------------------------------------------------------
    # Логика для Смены конкретного компонента у корабля
    # ---------------------------------------------------------
    def _change_component(self, conn, ship, weapon, hull, engine,
                          all_weapons, all_hulls, all_engines):

        component = random.choice(["weapon", "hull", "engine"])
        print(f"\n[SHIP] {ship}: chosen component to change -> {component}")

        if component == "weapon":
            new_weapon = random.choice(all_weapons)
            print(f"[SHIP] {ship}: weapon {weapon} -> {new_weapon}")
            self._update_ship_component(conn, ship, "weapon", new_weapon)
            return new_weapon, hull, engine

        elif component == "hull":
            new_hull = random.choice(all_hulls)
            print(f"[SHIP] {ship}: hull {hull} -> {new_hull}")
            self._update_ship_component(conn, ship, "hull", new_hull)
            return weapon, new_hull, engine

        else:
            new_engine = random.choice(all_engines)
            print(f"[SHIP] {ship}: engine {engine} -> {new_engine}")
            self._update_ship_component(conn, ship, "engine", new_engine)
            return weapon, hull, new_engine

    # ---------------------------------------------------------
    # Основной метод рандомизации - подробно описал в readme (Пояснение к выполнению работы)
    # ---------------------------------------------------------
    def _randomize(self, conn):
        ships, all_weapons, all_hulls, all_engines = self._load_data(conn)

        changed_weapons = set()
        changed_hulls = set()
        changed_engines = set()

        print(f"[INFO] Total ships: {len(ships)}")
        print(f"[INFO] Weapons: {len(all_weapons)}, hulls: {len(all_hulls)}, engines: {len(all_engines)}")

        for ship, weapon, hull, engine in ships:
            print("\n======================================")
            print(f"[SHIP] Processing {ship}")
            print(f"[SHIP] initial: weapon={weapon}, hull={hull}, engine={engine}")

            # A. Меняем один рандомный компонент
            weapon, hull, engine = self._change_component(
                conn, ship, weapon, hull, engine,
                all_weapons, all_hulls, all_engines
            )

            print(f"[SHIP] after component change: weapon={weapon}, hull={hull}, engine={engine}")

            # B. Меняем параметры ТЕКУЩИХ компонентов если не были изменены (только один раз)
            self._update_component_param_once(
                conn, weapon, changed_weapons,
                table="weapons",
                key_column="weapon",
                fields=["reload_speed", "rotational_speed", "diameter", "power_volley", "count"]
            )

            self._update_component_param_once(
                conn, hull, changed_hulls,
                table="hulls",
                key_column="hull",
                fields=["armor", "type", "capacity"]
            )

            self._update_component_param_once(
                conn, engine, changed_engines,
                table="engines",
                key_column="engine",
                fields=["power", "type"]
            )
