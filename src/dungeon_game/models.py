from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    description: str


@dataclass
class Potion(Item):
    heal_amount: int = 20


@dataclass
class Key(Item):
    unlocks: str = ""  # room_id where this key is used


@dataclass
class Character:
    name: str
    health: int = 100
    attack: int = 10


@dataclass
class Player(Character):
    inventory: list[Item] = field(default_factory=list)


@dataclass
class Monster(Character):
    health: int = 20
    attack: int = 5


@dataclass
class Room:
    id: str
    name: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)  # direction -> room_id
    items: list[Item] = field(default_factory=list)
    locked_exits: set[str] = field(default_factory=set)
    monsters: list[Monster] = field(default_factory=list)
