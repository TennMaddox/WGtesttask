import pytest

SHIP_IDS = [f"ship-{i}" for i in range(1, 201)]

WEAPON_FIELDS = [
    "reload_speed",
    "rotational_speed",
    "diameter",
    "power_volley",
    "count",
]

HULL_FIELDS = [
    "armor",
    "type",
    "capacity",
]

ENGINE_FIELDS = [
    "power",
    "type",
]


@pytest.mark.parametrize("ship_id", SHIP_IDS)
def test_weapon_for_ship(repos, ship_id):
    errors = []

    orig_ship = next(s for s in repos["orig_ships"].get_all_ships() if s.ship == ship_id)
    rnd_ship = next(s for s in repos["rnd_ships"].get_all_ships() if s.ship == ship_id)

    # Проверка: изменился ли компонент
    if orig_ship.weapon != rnd_ship.weapon:
        errors.append(
            f"{ship_id}, {rnd_ship.weapon}\n"
            f"    expected {orig_ship.weapon}, was {rnd_ship.weapon}"
        )

    orig_weapon = repos["orig_weapons"].get_by_name(orig_ship.weapon)
    rnd_weapon = repos["rnd_weapons"].get_by_name(rnd_ship.weapon)

    # Проверка: изменились ли параметры
    for field in WEAPON_FIELDS:
        ov = getattr(orig_weapon, field)
        rv = getattr(rnd_weapon, field)
        if ov != rv:
            errors.append(
                f"{ship_id}, {orig_weapon.weapon}\n"
                f"    {field.replace('_', ' ')}: expected {ov}, was {rv}"
            )

    if errors:
        pytest.fail("\n".join(errors))


@pytest.mark.parametrize("ship_id", SHIP_IDS)
def test_hull_for_ship(repos, ship_id):
    errors = []

    orig_ship = next(s for s in repos["orig_ships"].get_all_ships() if s.ship == ship_id)
    rnd_ship = next(s for s in repos["rnd_ships"].get_all_ships() if s.ship == ship_id)

    if orig_ship.hull != rnd_ship.hull:
        errors.append(
            f"{ship_id}, {rnd_ship.hull}\n"
            f"    expected {orig_ship.hull}, was {rnd_ship.hull}"
        )

    orig_hull = repos["orig_hulls"].get_by_name(orig_ship.hull)
    rnd_hull = repos["rnd_hulls"].get_by_name(rnd_ship.hull)

    for field in HULL_FIELDS:
        ov = getattr(orig_hull, field)
        rv = getattr(rnd_hull, field)
        if ov != rv:
            errors.append(
                f"{ship_id}, {orig_hull.hull}\n"
                f"    {field}: expected {ov}, was {rv}"
            )

    if errors:
        pytest.fail("\n".join(errors))


@pytest.mark.parametrize("ship_id", SHIP_IDS)
def test_engine_for_ship(repos, ship_id):
    errors = []

    orig_ship = next(s for s in repos["orig_ships"].get_all_ships() if s.ship == ship_id)
    rnd_ship = next(s for s in repos["rnd_ships"].get_all_ships() if s.ship == ship_id)

    if orig_ship.engine != rnd_ship.engine:
        errors.append(
            f"{ship_id}, {rnd_ship.engine}\n"
            f"    expected {orig_ship.engine}, was {rnd_ship.engine}"
        )

    orig_engine = repos["orig_engines"].get_by_name(orig_ship.engine)
    rnd_engine = repos["rnd_engines"].get_by_name(rnd_ship.engine)

    for field in ENGINE_FIELDS:
        ov = getattr(orig_engine, field)
        rv = getattr(rnd_engine, field)
        if ov != rv:
            errors.append(
                f"{ship_id}, {orig_engine.engine}\n"
                f"    {field}: expected {ov}, was {rv}"
            )

    if errors:
        pytest.fail("\n".join(errors))
