from src import Position, Direction
from src.game import Game, Map

if __name__ == '__main__':
    map = Map(4,4)
    game = Game(map, [Position(x=1,y=2)],234)
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.DOWN))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.UP))
    game.print()
    print(game.step(Direction.UP))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.DOWN))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.DOWN))
    game.print()

def test_snake_eating_itself():
    map = Map(4,4)
    game = Game(map, [Position(x=1,y=2)],234)
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.DOWN))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()
    print(game.step(Direction.UP))
    game.print()
    print(game.step(Direction.UP))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.RIGHT))
    game.print()
    print(game.step(Direction.DOWN))
    game.print()
    print(game.step(Direction.LEFT))
    game.print()

    # let snake eat itself
    print(game.step(Direction.UP))
    game.print()