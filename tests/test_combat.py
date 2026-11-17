import pytest
from dungeon_game.game import Game
from dungeon_game.models import Monster, Player



def _move_to_treasury(game: Game) -> None:
    game.move("north")  # -> hallway
    game.move("north")  # -> chamber
    game.take("iron key")
    game.use("iron key")
    game.move("north")  # -> treasury


def test_attack_damages_monster(game):
    _move_to_treasury(game)
    game.attack("goblin")
    goblin = game.rooms["treasury"].monsters[0]
    assert goblin.health == 20 - game.player.attack


def test_killing_monster_removes_it_from_room(game):
    _move_to_treasury(game)
    game.player.attack = 100  # one-shot
    game.attack("goblin")
    assert game.rooms["treasury"].monsters == []


def test_monster_counterattacks_player(game):
    _move_to_treasury(game)
    starting_health = game.player.health
    game.attack("goblin")
    assert game.player.health == starting_health - game.rooms["treasury"].monsters[0].attack


def test_attack_no_monster_in_room_returns_error(game):
    result = game.attack("goblin")
    assert "no" in result.lower()


def test_attack_unknown_monster_name_returns_error(game):
    _move_to_treasury(game)
    result = game.attack("dragon")
    assert "no" in result.lower()


def test_player_is_dead_false_at_start(game):
    assert not game.player_is_dead()


def test_player_is_dead_true_when_health_zero(game):
    game.player.health = 0
    assert game.player_is_dead()


def test_look_shows_monsters_in_room(game):
    _move_to_treasury(game)
    result = game.look()
    assert "Goblin" in result


def test_handle_command_attack(game):
    _move_to_treasury(game)
    result = game.handle_command("attack goblin")
    assert "goblin" in result.lower()
