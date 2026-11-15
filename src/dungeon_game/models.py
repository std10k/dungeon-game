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
