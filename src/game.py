import random
import time
from typing import List

import numpy as np

from src import Direction, Position


class Map:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.map = np.zeros([n, m], dtype=int)

    def get(self, pos: Position) -> int:
        return self.map[pos.x][pos.y]

    def set(self, pos: Position, value: int):
        self.map[pos.x][pos.y] = value

    def print(self):
        for j in range(self.m):
            s = ""
            for i in range(self.n):
                cell = self.map[i][j]
                s += str(cell) + " "
            print(s)


class Game:
    def __init__(self, map: Map, snake: List[Position], seed=time.time()):
        random.seed(seed)
        self.map = map
        self.snake = snake
        self.position = self.snake[0]
        for pos in snake:
            self.map.set(pos, 1)
        self.fruit = self.place_fruit()

    def step(self, action: Direction):
        new_pos = self.position.move(action)
        if new_pos.x < 0 or new_pos.y < 0 or new_pos.x >= self.map.n or new_pos.y >= self.map.m:
            return False
        else:
            if self.fruit == new_pos:
                # eat
                self.snake.append(new_pos)
                self.map.set(new_pos, len(self.snake))
                self.position = new_pos
                self.fruit = self.place_fruit()
            elif new_pos in self.snake:
                # snake eats itself
                return False
            else:
                # move
                self.map.set(new_pos, len(self.snake))
                self.position = new_pos
                for pos in self.snake:
                    value = self.map.get(pos)
                    value -= 1
                    self.map.set(pos, value)
                self.snake.append(new_pos)
                self.snake.reverse()
                self.snake.pop()
                self.snake.reverse()
            return True

    def place_fruit(self, pos: Position = None):
        if pos is None:
            pos = Position.random(self.map.n, self.map.m)

        while pos in self.snake:
            pos = Position.random(self.map.n, self.map.m)

        self.map.set(pos, -1)
        return pos

    def print(self):
        print("--------------------")
        self.map.print()
        print("--------------------")
