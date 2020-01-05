import random
from enum import Enum
from typing import Tuple


class Direction(Enum):
    UP = (1, (0, -1))
    RIGHT = (2, (1, 0))
    DOWN = (3, (0, 1))
    LEFT = (4, (-1, 0))

    def __init__(self, value: int, direction_vector: Tuple[int, int]):
        self.direction_vector = direction_vector

    def delta(self):
        return self.direction_vector


class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, direction: Direction):
        x = self.x + direction.direction_vector[0]
        y = self.y + direction.direction_vector[1]
        return Position(x=x, y=y)

    @staticmethod
    def random(n,m):
        x = random.randint(0, n-1)
        y = random.randint(0, m-1)
        return Position(x=x, y=y)

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False