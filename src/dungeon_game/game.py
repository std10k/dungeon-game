from dungeon_game.models import Item, Key, Player, Potion, Room
from dungeon_game.world import build_map

DIRECTIONS = {"north", "south", "east", "west"}


class Game:
    def __init__(self, player: Player) -> None:
        self.rooms: dict[str, Room] = build_map()
        self.player = player
        self.current_room_id = "entrance"

    def look(self) -> str:
        room = self.rooms[self.current_room_id]
        exits = ", ".join(room.exits.keys()) if room.exits else "none"
        lines = [room.name, room.description, f"Exits: {exits}"]
        if room.items:
            item_names = ", ".join(item.name for item in room.items)
            lines.append(f"Items: {item_names}")
        return "\n".join(lines)

    def move(self, direction: str) -> str:
        room = self.rooms[self.current_room_id]
        if direction not in room.exits:
            return f"You can't go {direction} from here."
        if direction in room.locked_exits:
            return "That way is locked."
        self.current_room_id = room.exits[direction]
        return self.look()

    def take(self, name: str) -> str:
        room = self.rooms[self.current_room_id]
        item = self._find_item(room.items, name)
        if item is None:
            return f"There is no '{name}' here."
        room.items.remove(item)
        self.player.inventory.append(item)
        return f"You pick up the {item.name}."

    def drop(self, name: str) -> str:
        item = self._find_item(self.player.inventory, name)
        if item is None:
            return f"You don't have a '{name}'."
        self.player.inventory.remove(item)
        self.rooms[self.current_room_id].items.append(item)
        return f"You drop the {item.name}."

    def use(self, name: str) -> str:
        item = self._find_item(self.player.inventory, name)
        if item is None:
            return f"You don't have a '{name}'."
        if isinstance(item, Potion):
            self.player.health += item.heal_amount
            self.player.inventory.remove(item)
            return f"You drink the {item.name} and restore {item.heal_amount} health. (Health: {self.player.health})"
        if isinstance(item, Key):
            room = self.rooms[self.current_room_id]
            if item.unlocks == self.current_room_id and room.locked_exits:
                room.locked_exits.clear()
                self.player.inventory.remove(item)
                return f"You use the {item.name}. You hear a click — the way is now open."
            return "This key doesn't work here."
        return f"You can't use the {item.name}."

    def handle_command(self, raw: str) -> str:
        parts = raw.strip().lower().split()
        if not parts:
            return "What?"
        if parts[0] == "quit":
            return "__quit__"
        if parts[0] == "look":
            return self.look()
        if parts[0] == "go" and len(parts) > 1:
            return self.move(parts[1])
        if parts[0] in DIRECTIONS:
            return self.move(parts[0])
        if parts[0] in ("take", "drop", "use") and len(parts) > 1:
            item_name = " ".join(parts[1:])
            if parts[0] == "take":
                return self.take(item_name)
            if parts[0] == "drop":
                return self.drop(item_name)
            return self.use(item_name)
        return f"Unknown command: {raw.strip()!r}"

    def is_over(self) -> bool:
        return self.current_room_id == "exit"

    @staticmethod
    def _find_item(items: list[Item], name: str) -> Item | None:
        for item in items:
            if item.name.lower() == name.lower():
                return item
        return None
