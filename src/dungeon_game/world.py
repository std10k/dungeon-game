import random

from dungeon_game.models import Key, Monster, Potion, Room

_OPPOSITES = {"north": "south", "south": "north", "east": "west", "west": "east"}

_MAIN_ROOM_POOL = [
    ("Stone Corridor", "A passage with crumbling stone walls."),
    ("Guard Post", "A room that once housed dungeon guards."),
    ("Rotting Chapel", "A small chapel with broken pews."),
    ("Armory", "Rusted weapons line the walls."),
    ("Great Hall", "A vast hall with a vaulted ceiling."),
    ("Bone Chamber", "Skulls and bones are piled in the corners."),
    ("Ancient Vault", "An ancient vault with heavy stone doors."),
    ("Forgotten Passage", "A forgotten passage smelling of decay."),
]

_DEAD_END_POOL = [
    ("Bone Pit", "A pit filled with bleached bones."),
    ("Storage Alcove", "A dusty alcove with broken shelves."),
    ("Dark Cellar", "A damp cellar with a low ceiling."),
    ("Alchemy Nook", "A room with shattered alchemical apparatus."),
    ("Flooded Chamber", "The floor is covered in stagnant water."),
    ("Crumbling Shrine", "A crumbling shrine to a forgotten god."),
    ("Rat's Nest", "Rats scurry in the shadows."),
    ("Abandoned Cell", "An abandoned cell with rusted bars."),
]

_MONSTER_POOL = [
    ("Goblin", 20, 5),
    ("Skeleton", 15, 7),
    ("Rat", 10, 3),
    ("Zombie", 25, 6),
    ("Orc", 30, 8),
]

_POTION_POOL = [
    ("Health Potion", "A small vial of red liquid.", 20),
    ("Elixir", "A glowing bottle with a sweet smell.", 30),
    ("Tonic", "A murky brown liquid.", 15),
]


def build_map(seed: int | None = None) -> dict[str, Room]:
    """Generate a fresh 10-room dungeon: 5 on the main path, 5 dead ends."""
    if seed is not None:
        random.seed(seed)

    # --- Main path rooms ---
    middle_templates = random.sample(_MAIN_ROOM_POOL, 3)
    path_ids = ["entrance", "main_1", "main_2", "main_3", "exit"]

    rooms: dict[str, Room] = {
        "entrance": Room(id="entrance", name="Entrance",
                         description="A dimly lit entrance to the dungeon."),
        "main_1":   Room(id="main_1",   name=middle_templates[0][0],
                         description=middle_templates[0][1]),
        "main_2":   Room(id="main_2",   name=middle_templates[1][0],
                         description=middle_templates[1][1]),
        "main_3":   Room(id="main_3",   name=middle_templates[2][0],
                         description=middle_templates[2][1],
                         locked_exits={"north"}),
        "exit":     Room(id="exit",     name="Exit",
                         description="A heavy iron door leads out of the dungeon."),
    }

    # Wire north-south exits along the main path
    for i in range(len(path_ids) - 1):
        a, b = path_ids[i], path_ids[i + 1]
        rooms[a].exits["north"] = b
        rooms[b].exits["south"] = a

    # --- Dead ends ---
    # 8 possible (room, direction) slots; pick 5 without repetition
    slots = [(rid, d) for rid in ["entrance", "main_1", "main_2", "main_3"]
             for d in ["east", "west"]]
    random.shuffle(slots)
    chosen_slots = slots[:5]
    dead_templates = random.sample(_DEAD_END_POOL, 5)

    for i, (main_id, direction) in enumerate(chosen_slots):
        dead_id = f"dead_{i}"
        back = _OPPOSITES[direction]
        dead_room = Room(id=dead_id,
                         name=dead_templates[i][0],
                         description=dead_templates[i][1],
                         exits={back: main_id})
        rooms[main_id].exits[direction] = dead_id
        rooms[dead_id] = dead_room

    # --- Items ---
    # Key: must be in a room reachable before main_3
    pre_main3 = {"entrance", "main_1", "main_2"}
    pre_main3 |= {
        dead_id for dead_id in rooms
        if dead_id.startswith("dead_")
        and any(v in pre_main3 for v in rooms[dead_id].exits.values())
    }
    key_room_id = random.choice(sorted(pre_main3))
    rooms[key_room_id].items.append(
        Key(name="Iron Key", description="A heavy iron key.", unlocks="main_3")
    )

    # Potions: 2, in any non-entrance non-exit room
    item_eligible = ["main_1", "main_2", "main_3"] + [r for r in rooms if r.startswith("dead_")]
    potion_rooms = random.sample(item_eligible, min(2, len(item_eligible)))
    potion_templates = random.choices(_POTION_POOL, k=2)
    for room_id, (name, desc, heal) in zip(potion_rooms, potion_templates):
        rooms[room_id].items.append(Potion(name=name, description=desc, heal_amount=heal))

    # Monsters: 2, in any non-entrance non-exit room
    monster_eligible = ["main_1", "main_2", "main_3"] + [r for r in rooms if r.startswith("dead_")]
    monster_rooms = random.sample(monster_eligible, min(2, len(monster_eligible)))
    monster_templates = random.sample(_MONSTER_POOL, 2)
    for room_id, (name, health, attack) in zip(monster_rooms, monster_templates):
        rooms[room_id].monsters.append(Monster(name=name, health=health, attack=attack))

    return rooms
