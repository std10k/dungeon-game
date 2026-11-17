from dungeon_game.models import Key, Potion
from dungeon_game.world import build_map


def _main_path_ids():
    return ["entrance", "main_1", "main_2", "main_3", "exit"]


def _dead_end_ids(rooms):
    return [rid for rid in rooms if rid.startswith("dead_")]


def _find_key_room(rooms):
    for room_id, room in rooms.items():
        for item in room.items:
            if isinstance(item, Key):
                return room_id
    return None


def test_build_map_returns_ten_rooms():
    rooms = build_map(seed=0)
    assert len(rooms) == 10


def test_five_main_path_rooms_exist():
    rooms = build_map(seed=0)
    for rid in _main_path_ids():
        assert rid in rooms


def test_five_dead_end_rooms_exist():
    rooms = build_map(seed=0)
    assert len(_dead_end_ids(rooms)) == 5


def test_main_path_connected_north_south():
    rooms = build_map(seed=0)
    path = _main_path_ids()
    for i in range(len(path) - 1):
        assert rooms[path[i]].exits.get("north") == path[i + 1]
        assert rooms[path[i + 1]].exits.get("south") == path[i]


def test_dead_ends_connect_east_west_to_main_path():
    rooms = build_map(seed=0)
    main_ids = set(_main_path_ids())
    for dead_id in _dead_end_ids(rooms):
        dead_room = rooms[dead_id]
        # Dead end's exit must be east or west, leading to a main-path room
        for direction, target in dead_room.exits.items():
            assert direction in ("east", "west")
            assert target in main_ids


def test_main3_north_exit_always_locked():
    rooms = build_map(seed=0)
    assert "north" in rooms["main_3"].locked_exits


def test_key_placed_before_main3():
    rooms = build_map(seed=0)
    key_room = _find_key_room(rooms)
    assert key_room is not None
    # Key must be in entrance, main_1, main_2, or dead ends attached to them
    pre_main3 = {"entrance", "main_1", "main_2"}
    pre_main3 |= {
        dead_id for dead_id in _dead_end_ids(rooms)
        if any(v in pre_main3 for v in rooms[dead_id].exits.values())
    }
    assert key_room in pre_main3


def test_at_least_one_monster():
    rooms = build_map(seed=0)
    total_monsters = sum(len(room.monsters) for room in rooms.values())
    assert total_monsters >= 1


def test_at_least_one_potion():
    rooms = build_map(seed=0)
    total_potions = sum(
        1 for room in rooms.values()
        for item in room.items if isinstance(item, Potion)
    )
    assert total_potions >= 1


def test_same_seed_produces_same_world():
    rooms_a = build_map(seed=42)
    rooms_b = build_map(seed=42)
    assert list(rooms_a.keys()) == list(rooms_b.keys())
    for rid in rooms_a:
        assert rooms_a[rid].name == rooms_b[rid].name
        assert rooms_a[rid].exits == rooms_b[rid].exits


def test_different_seeds_produce_different_worlds():
    rooms_a = build_map(seed=1)
    rooms_b = build_map(seed=2)
    names_a = {rid: r.name for rid, r in rooms_a.items()}
    names_b = {rid: r.name for rid, r in rooms_b.items()}
    assert names_a != names_b


def test_no_monsters_in_entrance_or_exit():
    rooms = build_map(seed=0)
    assert rooms["entrance"].monsters == []
    assert rooms["exit"].monsters == []


def test_all_exits_point_to_valid_rooms():
    rooms = build_map(seed=0)
    for room in rooms.values():
        for target_id in room.exits.values():
            assert target_id in rooms
