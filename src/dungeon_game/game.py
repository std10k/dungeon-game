import random

from dungeon_game.models import Item, Key, Monster, Player, Potion, Room
from dungeon_game.world import build_map

DIRECTIONS = {"north", "south", "east", "west"}
OPPOSITES = {"north": "south", "south": "north", "east": "west", "west": "east"}


class Game:
    def __init__(self, player: Player, rooms: dict[str, Room] | None = None,
                 seed: int | None = None) -> None:
        self.rooms: dict[str, Room] = rooms if rooms is not None else build_map(seed=seed)
        self.player = player
        self.current_room_id = "entrance"
        self.entry_direction: str | None = None
        self.first_use_in_room: bool = True

    def look(self) -> str:
        room = self.rooms[self.current_room_id]
        exits = ", ".join(room.exits.keys()) if room.exits else "none"
        lines = [room.name, room.description, f"Exits: {exits}"]
        if room.items:
            lines.append(f"Items: {', '.join(item.name for item in room.items)}")
        if room.monsters:
            lines.append(f"Monsters: {', '.join(m.name for m in room.monsters)}")
        return "\n".join(lines)

    def move(self, direction: str) -> str:
        room = self.rooms[self.current_room_id]
        if direction not in room.exits:
            return f"You can't go {direction} from here."
        if direction in room.locked_exits:
            return "That way is locked."
        if room.monsters and direction != self.entry_direction:
            monster = random.choice(room.monsters)
            self.player.health -= monster.attack
            self.first_use_in_room = False
            lines = [
                f"You try to flee! The {monster.name} strikes you for {monster.attack} damage."
                f" (Your health: {max(0, self.player.health)})"
            ]
            if self.player.health <= 0:
                lines.append("You have been defeated...")
            return "\n".join(lines)
        self.current_room_id = room.exits[direction]
        self.entry_direction = OPPOSITES.get(direction)
        self.first_use_in_room = True
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
            result = f"You drink the {item.name} and restore {item.heal_amount} health. (Health: {self.player.health})"
            return self._complete_turn(result)
        if isinstance(item, Key):
            room = self.rooms[self.current_room_id]
            if item.unlocks == self.current_room_id and room.locked_exits:
                room.locked_exits.clear()
                self.player.inventory.remove(item)
                result = f"You use the {item.name}. You hear a click — the way is now open."
                return self._complete_turn(result)
            return "This key doesn't work here."
        return f"You can't use the {item.name}."

    def _complete_turn(self, action_result: str) -> str:
        room = self.rooms[self.current_room_id]
        if not room.monsters:
            return action_result
        if self.first_use_in_room:
            self.first_use_in_room = False
            return action_result
        return action_result + "\n" + self._monster_counterattack()

    def _monster_counterattack(self) -> str:
        room = self.rooms[self.current_room_id]
        monster = random.choice(room.monsters)
        self.player.health -= monster.attack
        lines = [
            f"The {monster.name} seizes the moment and attacks you for {monster.attack} damage."
            f" (Your health: {max(0, self.player.health)})"
        ]
        if self.player.health <= 0:
            lines.append("You have been defeated...")
        return "\n".join(lines)

    def attack(self, monster_name: str) -> str:
        room = self.rooms[self.current_room_id]
        monster = next((m for m in room.monsters if m.name.lower() == monster_name.lower()), None)
        if monster is None:
            return f"There is no '{monster_name}' here to attack."
        self.first_use_in_room = False
        lines = []
        monster.health -= self.player.attack
        lines.append(
            f"You attack the {monster.name} for {self.player.attack} damage."
            f" ({monster.name} health: {max(0, monster.health)})"
        )
        if monster.health <= 0:
            room.monsters.remove(monster)
            lines.append(f"The {monster.name} is defeated!")
            return "\n".join(lines)
        self.player.health -= monster.attack
        lines.append(
            f"The {monster.name} attacks you for {monster.attack} damage."
            f" (Your health: {max(0, self.player.health)})"
        )
        if self.player.health <= 0:
            lines.append("You have been defeated...")
        return "\n".join(lines)

    def player_is_dead(self) -> bool:
        return self.player.health <= 0

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
        if parts[0] in ("take", "drop", "use", "attack") and len(parts) > 1:
            target = " ".join(parts[1:])
            if parts[0] == "take":
                return self.take(target)
            if parts[0] == "drop":
                return self.drop(target)
            if parts[0] == "use":
                return self.use(target)
            return self.attack(target)
        return f"Unknown command: {raw.strip()!r}"

    def is_over(self) -> bool:
        return self.current_room_id == "exit"

    @staticmethod
    def _find_item(items: list[Item], name: str) -> Item | None:
        for item in items:
            if item.name.lower() == name.lower():
                return item
        return None
