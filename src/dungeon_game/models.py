from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    description: str


@dataclass
class Player:
    name: str
    health: int = 100
    inventory: list[Item] = field(default_factory=list)


@dataclass
class Potion(Item):
    heal_amount: int = 20


@dataclass
class Key(Item):
    unlocks: str = ""  # room_id where this key is used


@dataclass
class Room:
    id: str
    name: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)  # direction -> room_id
    items: list[Item] = field(default_factory=list)
    locked_exits: set[str] = field(default_factory=set)
