from dungeon_game.models import Key, Potion, Room


def build_map() -> dict[str, Room]:
    """Return a dict of room_id -> Room for a five-room dungeon."""
    rooms = [
        Room(
            id="entrance",
            name="Entrance",
            description="A dimly lit entrance to the dungeon.",
            exits={"north": "hallway"},
        ),
        Room(
            id="hallway",
            name="Hallway",
            description="A long stone hallway with torches on the walls.",
            exits={"south": "entrance", "north": "chamber"},
            items=[Potion(name="Health Potion", description="A small vial of red liquid.")],
        ),
        Room(
            id="chamber",
            name="Chamber",
            description="A wide chamber with a cracked stone floor.",
            exits={"south": "hallway", "north": "treasury"},
            items=[Key(name="Iron Key", description="A heavy iron key.", unlocks="chamber")],
            locked_exits={"north"},
        ),
        Room(
            id="treasury",
            name="Treasury",
            description="A room filled with dusty chests.",
            exits={"south": "chamber", "north": "exit"},
        ),
        Room(
            id="exit",
            name="Exit",
            description="A heavy iron door leads out of the dungeon.",
            exits={"south": "treasury"},
        ),
    ]
    return {room.id: room for room in rooms}
