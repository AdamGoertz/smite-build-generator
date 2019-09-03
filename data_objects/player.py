from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
    name: str
    id: int

@dataclass(frozen=True)
class ProPlayer(Player):
    team: str
    role: str
