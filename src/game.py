import random
import time
from typing import List

import numpy as np

from src import Direction, Position


class GameMap:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.game_map = np.zeros([n, m], dtype=int)

    def get(self, pos: Position) -> int:
        return self.game_map[pos.x][pos.y]

    def set(self, pos: Position, value: int):
        self.game_map[pos.x][pos.y] = value

    def print(self):
        for j in range(self.m):
            s = ""
            for i in range(self.n):
                cell = self.game_map[i][j]
                s += str(cell) + " "
            print(s)

    def contains(self, pos: Position):
        return not (pos.x < 0 or pos.y < 0 or pos.x >= self.n or pos.y >= self.m)



class Game:
    def __init__(self, game_map: GameMap, snake: List[Position], seed=time.time()):
        # random.seed(seed)
        self.game_map = game_map
        self.snake = snake
        self.position = self.snake[0]
        for pos in snake:
            self.game_map.set(pos, 1)
        self.fruit = self.place_fruit()

    def step(self, action: Direction) -> int:
        new_pos = self.position.move(action)
        if new_pos.x < 0 or new_pos.y < 0 or new_pos.x >= self.game_map.n or new_pos.y >= self.game_map.m:
            return -1
        else:
            if self.fruit == new_pos:
                # eat
                self.snake.append(new_pos)
                self.game_map.set(new_pos, len(self.snake))
                self.position = new_pos
                self.fruit = self.place_fruit()
                return 3
            elif new_pos in self.snake:
                # snake eats itself
                return -1
            else:
                # move
                self.game_map.set(new_pos, len(self.snake))
                self.position = new_pos
                for pos in self.snake:
                    value = self.game_map.get(pos)
                    value -= 1
                    self.game_map.set(pos, value)
                self.snake.append(new_pos)
                self.snake.reverse()
                self.snake.pop()
                self.snake.reverse()
                return 0.0000001

    def place_fruit(self, pos: Position = None):
        if pos is None:
            pos = Position.random(self.game_map.n, self.game_map.m)

        while pos in self.snake:
            pos = Position.random(self.game_map.n, self.game_map.m)
        self.game_map.set(pos, -1)
        return pos

    def print(self):
        print("--------------------")
        self.game_map.print()
        print("--------------------")
