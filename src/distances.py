import math
from dataclasses import dataclass
from typing import Optional, List

from src import Position, Direction
from src.game import Game, GameMap


@dataclass
class Distances:
    food: List[int]
    wall: List[int]
    body: List[int]

    def __hash__(self) -> int:
        a = self.food.copy()
        a.extend(self.wall)
        a.extend(self.body)
        hash = 0
        l = len(a) - 1
        for i in range(len(a)):
            potency = l - i
            hash += math.pow(a[i], potency)
        return int(hash)


def calculate_distances(game: Game) -> Distances:
    food = []
    wall = []
    body = []
    head_pos = game.snake[len(game.snake) - 1]
    no_collision_indicator = game.game_map.n
    for direction in Direction:
        food_symbol = -1
        distance = calculate_distance(head_pos, game.game_map, food_symbol, direction)
        if distance is None:
            distance = no_collision_indicator
        food.append(distance)
    for direction in Direction:
        pos = head_pos
        steps = 0
        while game.game_map.contains(pos):
            pos = pos.move(direction)
            steps += 1
        wall.append(steps)
    for direction in Direction:
        min = game.game_map.n + game.game_map.m
        for body_part in game.snake[1:]:
            distance = calculate_distance(head_pos, game.game_map, body_part, direction)
            if distance and distance < min:
                min = distance
        if min == game.game_map.n + game.game_map.m:
            min = no_collision_indicator
        body.append(min)
    return Distances(food, wall, body)


def calculate_distance(head_position: Position, game_map: GameMap, search: int, direction: Direction) -> Optional[int]:
    for i in range(game_map.n):
        for j in range(game_map.m):
            item_position = Position(x=i, y=j)
            if game_map.get(item_position) == search:
                pos = head_position
                steps = 0
                while game_map.contains(pos):
                    if pos == item_position:
                        return steps
                    else:
                        pos = pos.move(direction)
                        steps += 1
                return None
    return None
