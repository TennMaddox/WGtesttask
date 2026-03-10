from dataclasses import dataclass


@dataclass
class Weapon:
    weapon: str
    reload_speed: int
    rotational_speed: int
    diameter: int
    power_volley: int
    count: int