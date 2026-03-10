import sqlite3
from pathlib import Path

import pytest

from db.create_and_fill import create_and_fill
from db.randomizer import DatabaseRandomizer
from app.repositories.ShipRepository import ShipRepository
from app.repositories.WeaponRepository import WeaponRepository
from app.repositories.HullRepository import HullRepository
from app.repositories.EngineRepository import EngineRepository


@pytest.fixture(scope="session")
def original_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    db_path = tmp_path_factory.mktemp("db") / "original.sqlite"
    create_and_fill(db_path)
    return db_path


@pytest.fixture(scope="session")
def randomized_db(original_db: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    rnd_path = tmp_path_factory.mktemp("db") / "randomized.sqlite"
    randomizer = DatabaseRandomizer(original_db, rnd_path)
    randomizer.create_randomized_copy()
    return rnd_path


@pytest.fixture
def original_conn(original_db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(original_db)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def randomized_conn(randomized_db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(randomized_db)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def repos(original_conn, randomized_conn):
    return {
        "orig_ships": ShipRepository(original_conn),
        "orig_weapons": WeaponRepository(original_conn),
        "orig_hulls": HullRepository(original_conn),
        "orig_engines": EngineRepository(original_conn),
        "rnd_ships": ShipRepository(randomized_conn),
        "rnd_weapons": WeaponRepository(randomized_conn),
        "rnd_hulls": HullRepository(randomized_conn),
        "rnd_engines": EngineRepository(randomized_conn),
    }
