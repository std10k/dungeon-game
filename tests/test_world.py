from dungeon_game.world import build_map


def test_build_map_returns_five_rooms():
    rooms = build_map()
    assert len(rooms) == 5


def test_all_exits_point_to_valid_rooms():
    rooms = build_map()
    for room in rooms.values():
        for target_id in room.exits.values():
            assert target_id in rooms, f"{room.id} exit points to unknown room '{target_id}'"


def test_connections_are_bidirectional():
    rooms = build_map()
    for room in rooms.values():
        for target_id in room.exits.values():
            target = rooms[target_id]
            assert any(dest == room.id for dest in target.exits.values()), (
                f"{room.id} -> {target_id} has no reverse connection"
            )
