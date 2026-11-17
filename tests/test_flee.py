import pytest
from dungeon_game.game import Game
from dungeon_game.models import Player



def _move_to_treasury(game: Game) -> None:
    game.move("north")        # -> hallway
    game.move("north")        # -> chamber
    game.take("iron key")
    game.use("iron key")
    game.move("north")        # -> treasury (entry_direction = "south")


def test_entry_direction_none_at_start(game):
    assert game.entry_direction is None


def test_move_sets_entry_direction_to_opposite(game):
    game.move("north")  # -> hallway
    assert game.entry_direction == "south"


def test_retreat_through_entry_direction_allowed(game):
    _move_to_treasury(game)
    game.move("south")  # retreat to chamber
    assert game.current_room_id == "chamber"


def test_blocked_exit_keeps_player_in_room(game):
    _move_to_treasury(game)
    game.move("north")  # blocked — monsters alive, north != entry_direction (south)
    assert game.current_room_id == "treasury"


def test_blocked_exit_provokes_attack(game):
    _move_to_treasury(game)
    starting_health = game.player.health
    result = game.move("north")
    assert game.player.health < starting_health
    assert "strikes" in result.lower()


def test_provoked_attack_can_kill_player(game):
    _move_to_treasury(game)
    game.player.health = 1  # one hit will kill
    game.move("north")
    assert game.player_is_dead()


def test_after_killing_monsters_all_exits_free(game):
    _move_to_treasury(game)
    game.player.attack = 100
    game.attack("goblin")
    game.move("north")  # no monsters — should succeed
    assert game.current_room_id == "exit"


def test_entry_direction_updates_on_retreat(game):
    _move_to_treasury(game)        # entry_direction = "south"
    game.move("south")             # retreat to chamber; entry_direction = "north"
    assert game.entry_direction == "north"
