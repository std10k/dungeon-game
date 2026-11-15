from dungeon_game.game import Game
from dungeon_game.models import Player
from dungeon_game.save import load_game, save_game

DEFAULT_SAVE = "savegame.json"


def run() -> None:
    game = Game(player=Player(name="Hero"))
    print(game.look())
    while not game.is_over():
        try:
            raw = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nFarewell.")
            break

        parts = raw.strip().lower().split()
        if parts and parts[0] == "save":
            filename = parts[1] if len(parts) > 1 else DEFAULT_SAVE
            save_game(game, filename)
            print(f"Game saved to {filename}.")
            continue
        if parts and parts[0] == "load":
            filename = parts[1] if len(parts) > 1 else DEFAULT_SAVE
            try:
                game = load_game(filename)
                print(f"Game loaded from {filename}.")
                print(game.look())
            except FileNotFoundError:
                print(f"No save file found: {filename}")
            continue

        result = game.handle_command(raw)
        if result == "__quit__":
            print("Farewell.")
            break
        print(result)
        if game.player_is_dead():
            print("Game over.")
            break
        if game.is_over():
            print("You have escaped the dungeon. You win!")
