from dungeon_game.game import Game
from dungeon_game.models import Player


def run() -> None:
    game = Game(player=Player(name="Hero"))
    print(game.look())
    while not game.is_over():
        try:
            raw = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nFarewell.")
            break
        result = game.handle_command(raw)
        if result == "__quit__":
            print("Farewell.")
            break
        print(result)
        if game.is_over():
            print("You have escaped the dungeon. You win!")
