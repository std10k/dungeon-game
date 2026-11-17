import json
from pathlib import Path

from dungeon_game.game import Game
from dungeon_game.models import Item, Key, Monster, Player, Potion, Room


def save_game(game: Game, path: str | Path) -> None:
    data = {
        "current_room_id": game.current_room_id,
        "entry_direction": game.entry_direction,
        "first_use_in_room": game.first_use_in_room,
        "player": {
            "name": game.player.name,
            "health": game.player.health,
            "attack": game.player.attack,
            "inventory": [_serialize_item(i) for i in game.player.inventory],
        },
        "rooms": {
            room_id: {
                "name": room.name,
                "description": room.description,
                "exits": room.exits,
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
    rooms = {
        room_id: _deserialize_room(room_id, room_data)
        for room_id, room_data in data["rooms"].items()
    }
    game = Game(player=player, rooms=rooms)
    game.current_room_id = data["current_room_id"]
    game.entry_direction = data.get("entry_direction")
    game.first_use_in_room = data.get("first_use_in_room", True)
    return game


def _deserialize_room(room_id: str, d: dict) -> Room:
    room = Room(
        id=room_id,
        name=d["name"],
        description=d["description"],
        exits=d["exits"],
    )
    room.items = [_deserialize_item(i) for i in d["items"]]
    room.locked_exits = set(d["locked_exits"])
    room.monsters = [_deserialize_monster(m) for m in d["monsters"]]
    return room


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
