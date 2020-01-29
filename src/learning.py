import random
from dataclasses import dataclass
from itertools import product
from time import sleep
from typing import Tuple, List, Optional

import numpy as np

from src import Direction, Position
from src.distances import Distances, calculate_distances
from src.game import GameMap, Game


class Table:

    def __init__(self, n: int, q_table=None, index=None, lookup=None):
        self.n = n
        if q_table is not None:
            self.q_table = q_table
            self.index = index
            self.lookup_map = lookup
        else:
            possible_numbers = [n]
            possible_numbers.extend(range(n))
            perms1 = list(product(possible_numbers, repeat=4))
            possible_states = len(perms1) ** 3
            self.q_table = np.ones((int(possible_states),4))
            self.index = 0
            self.lookup_map = dict()

    def get_value(self, state: Distances, action: Direction) -> float:
        index = self.lookup_map.get(state)
        if index is None:
            index = self.index
            self.index += 1
            self.lookup_map[state] = index
        return self.q_table[index, action.key]

    def set_value(self, distances: Distances, action: Direction, value: float):
        index = self.lookup_map.get(distances)
        if index is None:
            index = self.index
            self.index += 1
            self.lookup_map[distances] = index
        self.q_table[index, action.key] = value

    def get_actions(self, distances: Distances) -> List[Tuple[Direction, float]]:
        index = self.lookup_map.get(distances)
        if index is None:
            index = self.index
            self.index += 1
            self.lookup_map[distances] = index
        action_values = self.q_table[index, :]
        actions = []
        for value, direction in zip(action_values, Direction):
            actions.append((direction, value))
        return actions


def save_table(table: Table):
    np.save('model', table.q_table)
    np.save('lookup', table.lookup_map, allow_pickle=True)
    with open('model-info.txt', 'w+') as f:
        f.write(f'{str(table.index)}\n')
        f.write(f'{str(table.n)}\n')


def load_table() -> Optional[Table]:
    try:
        q_table = np.load('model.npy')
        lookup = np.load('lookup.npy', allow_pickle=True).item()
        with open('model-info.txt', 'r') as f:
            index = int(f.readline())
            n = int(f.readline())
        return Table(n, q_table=q_table, lookup=lookup, index=index)
    except:
        return None


def take_action(state: Distances, table: Table) -> Direction:
    actions: List[Tuple[Direction, float]] = table.get_actions(state)
    max = None
    max_action = None
    for dir, value in actions:
        if max is None:
            max = value
            max_action = dir
        elif max < value:
            max = value
            max_action = dir

    if max_action is None:
        raise ValueError('Got no actions for state')
    return max_action


def value_iteration_update(old_value: float, learning_rate: float, reward: float, discount_factor: float,
                           estimated_future_value: float) -> float:
    return old_value + learning_rate * (reward + discount_factor * estimated_future_value - old_value)


@dataclass
class QLearningSettings:
    learning_rate: float
    discount_factor: float
    episodes: int
    epsilon: float
    current_episode: int


def update_state(action: Direction, table: Table, settings: QLearningSettings, game: Game):
    old_state = calculate_distances(game)
    old_value = table.get_value(old_state, action)
    reward = game.step(action)
    new_state = calculate_distances(game)
    best_next_action = take_action(new_state, table)
    estimated_future_value = table.get_value(new_state, best_next_action)
    update = value_iteration_update(
        old_value=old_value,
        learning_rate=settings.learning_rate,
        reward=reward,
        discount_factor=settings.discount_factor,
        estimated_future_value=estimated_future_value
    )
    table.set_value(old_state, action, update)
    return reward >= 0


def start_training(game: Game, table: Table, settings: QLearningSettings) -> Table:
    current_episode = 0
    highest_score = -1
    while current_episode < settings.episodes:
        current_state = calculate_distances(game)
        best_action = take_action(current_state, table)
        if random.random() < settings.epsilon:
            random_action = random.randint(0, 3)
            best_action = list(Direction)[random_action]
        success = update_state(best_action, table, settings, game)
        if not success:
            score = len(game.snake)
            print(f'Score: {score}')
            print(f'Epsiode: {current_episode + 1}')
            if highest_score < score:
                highest_score = score
            start = Position.random(game.game_map.n, game.game_map.n)
            game = Game(game.game_map, [start])
            current_episode += 1
    print(f'Highest Score: {highest_score}')
    return table


def test_table(table: Table, n: int):
    map = GameMap(n, n)
    game = Game(map, [Position.random(n, n)])
    # game = Game(map, [Position.random(n, n)])
    while True:
        print('Current State')
        game.print()
        current_state = calculate_distances(game)
        best_action = take_action(current_state, table)
        print(f'Action: {best_action}')
        result = game.step(best_action)
        print(f'Result of move: {result}')
        if result < 0:
            print('Game over')
            return
        sleep(2)


def main():
    n = 4
    settings = QLearningSettings(
        learning_rate=0.8,
        discount_factor=0.5,
        episodes=1000,
        epsilon=0.0001,
        current_episode=0
    )

    map = GameMap(n, n)
    game = Game(map, [Position(0,0)])
    table = load_table()
    if table is None:
        table = Table(n)
    table = start_training(game, table, settings)
    # save_table(table)
    test_table(table, n)


if __name__ == '__main__':
    main()
