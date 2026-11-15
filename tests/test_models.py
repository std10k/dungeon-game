from dungeon_game.models import Item, Player


def test_item():
    item = Item(name="Sword", description="A sharp blade")
    assert item.name == "Sword"
    assert item.description == "A sharp blade"


def test_player_defaults():
    player = Player(name="Hero")
    assert player.health == 100
    assert player.inventory == []


def test_player_custom_values():
    player = Player(name="Hero", health=50)
    assert player.health == 50


def test_player_inventory():
    sword = Item(name="Sword", description="A sharp blade")
    player = Player(name="Hero")
    player.inventory.append(sword)
    assert len(player.inventory) == 1
    assert player.inventory[0] == sword
