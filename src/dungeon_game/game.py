from dungeon_game.models import Player, Room
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
        return f"{room.name}\n{room.description}\nExits: {exits}"

    def move(self, direction: str) -> str:
        room = self.rooms[self.current_room_id]
        if direction not in room.exits:
            return f"You can't go {direction} from here."
        self.current_room_id = room.exits[direction]
        return self.look()

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
        return f"Unknown command: {raw.strip()!r}"

    def is_over(self) -> bool:
        return self.current_room_id == "exit"
