from dataclasses import dataclass
from .player import Player
from typing import Optional

@dataclass
class Team:
    name: str
    league: str
    solo: Optional[Player]
    jungle: Optional[Player]
    mid: Optional[Player]
    support: Optional[Player]
    adc: Optional[Player]