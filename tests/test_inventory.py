import pytest
from dungeon_game.game import Game
from dungeon_game.models import Player, Potion


@pytest.fixture
def game() -> Game:
    return Game(player=Player(name="Hero"))


def _move_to_hallway(game: Game) -> None:
    game.move("north")  # entrance -> hallway


def _move_to_chamber(game: Game) -> None:
    game.move("north")  # entrance -> hallway
    game.move("north")  # hallway -> chamber


def test_take_moves_item_to_inventory(game):
    _move_to_hallway(game)
    game.take("health potion")
    assert len(game.player.inventory) == 1
    assert game.rooms["hallway"].items == []


def test_take_unknown_item_returns_error(game):
    result = game.take("nonexistent")
    assert "no" in result.lower()
    assert game.player.inventory == []


def test_drop_moves_item_to_room(game):
    _move_to_hallway(game)
    game.take("health potion")
    game.drop("health potion")
    assert game.player.inventory == []
    assert len(game.rooms["hallway"].items) == 1


def test_use_potion_heals_player(game):
    _move_to_hallway(game)
    game.player.health = 50
    game.take("health potion")
    game.use("health potion")
    assert game.player.health == 70
    assert game.player.inventory == []


def test_move_into_locked_exit_returns_error(game):
    _move_to_chamber(game)
    result = game.move("north")
    assert "locked" in result.lower()
    assert game.current_room_id == "chamber"


def test_use_key_in_correct_room_unlocks_exit(game):
    _move_to_chamber(game)
    game.take("iron key")
    result = game.use("iron key")
    assert "open" in result.lower()
    assert game.player.inventory == []
    assert "north" not in game.rooms["chamber"].locked_exits


def test_use_key_in_wrong_room_returns_error(game):
    _move_to_chamber(game)
    game.take("iron key")
    game.move("south")  # back to hallway
    result = game.use("iron key")
    assert "doesn't work" in result.lower()
    assert len(game.player.inventory) == 1  # still have key


def test_move_after_using_key_succeeds(game):
    _move_to_chamber(game)
    game.take("iron key")
    game.use("iron key")
    game.move("north")
    assert game.current_room_id == "treasury"


def test_look_shows_items_in_room(game):
    _move_to_hallway(game)
    result = game.look()
    assert "Health Potion" in result
