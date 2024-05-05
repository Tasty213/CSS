from dataclasses import dataclass


@dataclass
class Environment:
    light: bool
    light_level: int
    movement: bool
    distance: int
