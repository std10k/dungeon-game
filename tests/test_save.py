import json
import pytest
from dungeon_game.game import Game
from dungeon_game.models import Key, Player, Potion
from dungeon_game.save import load_game, save_game



def test_save_creates_json_file(game, tmp_path):
    path = tmp_path / "save.json"
    save_game(game, path)
    assert path.exists()
    data = json.loads(path.read_text())
    assert "current_room_id" in data
    assert "player" in data
    assert "rooms" in data


def test_round_trip_restores_current_room(game, tmp_path):
    game.move("north")  # -> hallway
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert loaded.current_room_id == "hallway"


def test_round_trip_restores_player_health(game, tmp_path):
    game.player.health = 42
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert loaded.player.health == 42


def test_round_trip_restores_player_inventory_types(game, tmp_path):
    game.move("north")        # -> hallway
    game.take("health potion")
    game.move("north")        # -> chamber
    game.take("iron key")
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert len(loaded.player.inventory) == 2
    assert isinstance(loaded.player.inventory[0], Potion)
    assert isinstance(loaded.player.inventory[1], Key)


def test_round_trip_restores_room_items(game, tmp_path):
    game.move("north")        # -> hallway
    game.take("health potion")
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert loaded.rooms["hallway"].items == []


def test_round_trip_restores_locked_exits(game, tmp_path):
    game.move("north")        # -> hallway
    game.move("north")        # -> chamber
    game.take("iron key")
    game.use("iron key")      # unlocks north
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert "north" not in loaded.rooms["chamber"].locked_exits


def test_round_trip_restores_dead_monsters(game, tmp_path):
    game.move("north")
    game.move("north")
    game.take("iron key")
    game.use("iron key")
    game.move("north")        # -> treasury
    game.player.attack = 100
    game.attack("goblin")     # kills goblin
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    assert loaded.rooms["treasury"].monsters == []


def test_round_trip_restores_room_structure(game, tmp_path):
    path = tmp_path / "save.json"
    save_game(game, path)
    loaded = load_game(path)
    for room_id, room in game.rooms.items():
        assert room_id in loaded.rooms
        assert loaded.rooms[room_id].name == room.name
        assert loaded.rooms[room_id].description == room.description
        assert loaded.rooms[room_id].exits == room.exits
