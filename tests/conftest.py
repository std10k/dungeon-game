import pytest

from dungeon_game.game import Game
from dungeon_game.models import Key, Monster, Player, Potion, Room


def _make_legacy_world() -> dict[str, Room]:
    """The original fixed 5-room world used by all mechanic tests."""
    entrance = Room(id="entrance", name="Entrance",
                    description="A dimly lit entrance to the dungeon.",
                    exits={"north": "hallway"})
    hallway = Room(id="hallway", name="Hallway",
                   description="A long stone hallway with torches on the walls.",
                   exits={"south": "entrance", "north": "chamber"},
                   items=[Potion(name="Health Potion",
                                 description="A small vial of red liquid.")])
    chamber = Room(id="chamber", name="Chamber",
                   description="A wide chamber with a cracked stone floor.",
                   exits={"south": "hallway", "north": "treasury"},
                   items=[Key(name="Iron Key",
                              description="A heavy iron key.", unlocks="chamber")],
                   locked_exits={"north"})
    treasury = Room(id="treasury", name="Treasury",
                    description="A room filled with dusty chests.",
                    exits={"south": "chamber", "north": "exit"},
                    monsters=[Monster(name="Goblin", health=20, attack=5)])
    exit_room = Room(id="exit", name="Exit",
                     description="A heavy iron door leads out of the dungeon.",
                     exits={"south": "treasury"})
    return {r.id: r for r in [entrance, hallway, chamber, treasury, exit_room]}


@pytest.fixture
def game() -> Game:
    return Game(player=Player(name="Hero"), rooms=_make_legacy_world())
