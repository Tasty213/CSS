from dataclasses import dataclass
from random import randint, random


@dataclass
class Environment:
    light: bool
    light_level: int
    movement: bool
    distance: int


class RealisticEnvironment(Environment):
    def __init__(
        self,
        light_change_chance=0.3,
        light_level_range=[-20, 20],
        movement_change_chance=0.1,
        distance_range=[-40, 40],
    ):
        self.light_change_chance = light_change_chance
        self.light_level_range = light_level_range
        self.movement_change_chance = movement_change_chance
        self.distance_range = distance_range

        self.light = False
        self.distance = 20
        self.light_level = 10
        self.movement = False

    @property
    def light(self):
        if random() < self.light_change_chance:
            self.light = not self._light
        return self._light

    @light.setter
    def light(self, value):
        self._light = value

    @property
    def light_level(self):
        change = randint(self.light_level_range[0], self.light_level_range[1]) / 10
        self.light_level = self._light_level + int(change)
        return self._light_level

    @light_level.setter
    def light_level(self, value):
        self._light_level = value

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, value):
        self._movement = value

    @property
    def distance(self):
        change = randint(self.distance_range[0], self.distance_range[1]) / 10
        self.distance = self._distance + int(change)
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
