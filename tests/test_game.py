import pytest
from dungeon_game.game import Game
from dungeon_game.models import Player


@pytest.fixture
def game() -> Game:
    return Game(player=Player(name="Hero"))


def test_starts_at_entrance(game):
    assert game.current_room_id == "entrance"


def test_look_includes_room_name_and_exits(game):
    result = game.look()
    assert "Entrance" in result
    assert "north" in result


def test_move_north_reaches_hallway(game):
    game.move("north")
    assert game.current_room_id == "hallway"


def test_move_invalid_direction_returns_error(game):
    result = game.move("south")
    assert "can't" in result.lower()
    assert game.current_room_id == "entrance"


def test_handle_command_go_direction(game):
    game.handle_command("go north")
    assert game.current_room_id == "hallway"


def test_handle_command_bare_direction(game):
    game.handle_command("north")
    assert game.current_room_id == "hallway"


def test_handle_command_look(game):
    result = game.handle_command("look")
    assert "Entrance" in result


def test_is_over_false_at_start(game):
    assert not game.is_over()


def test_is_over_true_at_exit(game):
    game.move("north")  # -> hallway
    game.move("north")  # -> chamber
    game.take("iron key")
    game.use("iron key")  # unlock north
    game.move("north")  # -> treasury
    game.player.attack = 100
    game.attack("goblin")  # defeat goblin
    game.move("north")  # -> exit
    assert game.is_over()


def test_handle_command_quit(game):
    assert game.handle_command("quit") == "__quit__"
