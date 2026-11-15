import json
from pathlib import Path

from dungeon_game.game import Game
from dungeon_game.models import Item, Key, Monster, Player, Potion


def save_game(game: Game, path: str | Path) -> None:
    data = {
        "current_room_id": game.current_room_id,
        "player": {
            "name": game.player.name,
            "health": game.player.health,
            "attack": game.player.attack,
            "inventory": [_serialize_item(i) for i in game.player.inventory],
        },
        "rooms": {
            room_id: {
                "items": [_serialize_item(i) for i in room.items],
                "locked_exits": list(room.locked_exits),
                "monsters": [_serialize_monster(m) for m in room.monsters],
            }
            for room_id, room in game.rooms.items()
        },
    }
    Path(path).write_text(json.dumps(data, indent=2))


def load_game(path: str | Path) -> Game:
    data = json.loads(Path(path).read_text())
    player = Player(
        name=data["player"]["name"],
        health=data["player"]["health"],
        attack=data["player"]["attack"],
        inventory=[_deserialize_item(i) for i in data["player"]["inventory"]],
    )
    game = Game(player=player)
    game.current_room_id = data["current_room_id"]
    for room_id, room_data in data["rooms"].items():
        room = game.rooms[room_id]
        room.items = [_deserialize_item(i) for i in room_data["items"]]
        room.locked_exits = set(room_data["locked_exits"])
        room.monsters = [_deserialize_monster(m) for m in room_data["monsters"]]
    return game


def _serialize_item(item: Item) -> dict:
    d = {"type": type(item).__name__, "name": item.name, "description": item.description}
    if isinstance(item, Potion):
        d["heal_amount"] = item.heal_amount
    elif isinstance(item, Key):
        d["unlocks"] = item.unlocks
    return d


def _deserialize_item(d: dict) -> Item:
    t = d["type"]
    if t == "Potion":
        return Potion(name=d["name"], description=d["description"], heal_amount=d["heal_amount"])
    if t == "Key":
        return Key(name=d["name"], description=d["description"], unlocks=d["unlocks"])
    return Item(name=d["name"], description=d["description"])


def _serialize_monster(m: Monster) -> dict:
    return {"name": m.name, "health": m.health, "attack": m.attack}


def _deserialize_monster(d: dict) -> Monster:
    return Monster(name=d["name"], health=d["health"], attack=d["attack"])
