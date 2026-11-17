import pytest
from dungeon_game.game import Game
from dungeon_game.models import Player, Potion



def _move_to_treasury(game: Game) -> None:
    game.move("north")        # -> hallway
    game.move("north")        # -> chamber
    game.take("iron key")
    game.use("iron key")      # free first use (no monsters in chamber)
    game.move("north")        # -> treasury (goblin present); first_use_in_room reset


def test_use_in_room_with_no_monsters_no_attack(game):
    game.move("north")  # -> hallway (no monsters)
    game.take("health potion")
    result = game.use("health potion")
    assert "seizes" not in result


def test_first_use_in_monster_room_is_free(game):
    _move_to_treasury(game)
    game.player.inventory.append(Potion(name="Test Potion", description=".", heal_amount=5))
    result = game.use("test potion")
    assert "seizes" not in result


def test_first_use_sets_flag_to_false(game):
    _move_to_treasury(game)
    assert game.first_use_in_room is True
    game.player.inventory.append(Potion(name="Test Potion", description=".", heal_amount=5))
    game.use("test potion")
    assert game.first_use_in_room is False


def test_second_use_triggers_monster_attack(game):
    _move_to_treasury(game)
    game.player.inventory.append(Potion(name="Potion A", description=".", heal_amount=5))
    game.player.inventory.append(Potion(name="Potion B", description=".", heal_amount=5))
    game.use("potion a")  # free
    health_after_free = game.player.health
    game.use("potion b")  # triggers attack
    assert game.player.health < health_after_free + 5  # net: heal minus monster hit


def test_second_use_result_contains_attack_message(game):
    _move_to_treasury(game)
    game.player.inventory.append(Potion(name="Potion A", description=".", heal_amount=5))
    game.player.inventory.append(Potion(name="Potion B", description=".", heal_amount=5))
    game.use("potion a")
    result = game.use("potion b")
    assert "seizes" in result


def test_failed_use_does_not_consume_turn(game):
    _move_to_treasury(game)
    game.use("nonexistent")  # fails — no turn
    assert game.first_use_in_room is True


def test_failed_key_does_not_consume_turn(game):
    # bring a key to a room where it doesn't work
    game.move("north")        # -> hallway
    game.move("north")        # -> chamber
    game.take("iron key")
    game.move("south")        # -> hallway
    # first_use_in_room = True (just entered hallway)
    result = game.use("iron key")  # fails: key unlocks chamber, not hallway
    assert "doesn't work" in result
    assert game.first_use_in_room is True


def test_moving_to_new_room_resets_flag(game):
    _move_to_treasury(game)
    game.player.inventory.append(Potion(name="Test Potion", description=".", heal_amount=5))
    game.use("test potion")           # free, sets flag False
    assert game.first_use_in_room is False
    game.move("south")                # retreat to chamber
    assert game.first_use_in_room is True


def test_monster_counterattack_is_one_monster(game):
    _move_to_treasury(game)
    game.player.inventory.append(Potion(name="Potion A", description=".", heal_amount=0))
    game.player.inventory.append(Potion(name="Potion B", description=".", heal_amount=0))
    game.use("potion a")  # free
    health_before = game.player.health
    game.use("potion b")  # triggers exactly one monster attack
    goblin = game.rooms["treasury"].monsters[0]
    assert game.player.health == health_before - goblin.attack


def test_blocked_flee_closes_free_use_window(game):
    _move_to_treasury(game)
    game.move("north")  # blocked — provoked attack closes free-use window
    game.player.inventory.append(Potion(name="Test Potion", description=".", heal_amount=50))
    health_before = game.player.health
    game.use("test potion")  # should trigger counterattack
    goblin = game.rooms["treasury"].monsters[0]
    # health = health_before + 50 (heal) - goblin.attack (counterattack)
    assert game.player.health == health_before + 50 - goblin.attack


def test_attack_closes_free_use_window(game):
    _move_to_treasury(game)
    game.attack("goblin")  # attack closes free-use window (goblin survives — 10 dmg vs 20 hp)
    game.player.inventory.append(Potion(name="Test Potion", description=".", heal_amount=50))
    health_before = game.player.health
    game.use("test potion")  # should trigger counterattack
    goblin = game.rooms["treasury"].monsters[0]
    assert game.player.health == health_before + 50 - goblin.attack
