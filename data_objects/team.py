from dataclasses import dataclass
from .player import Player

@dataclass
class Team:
    name: str
    league: str
    solo: Player
    jungle: Player
    mid: Player
    support: Player
    adc: Player