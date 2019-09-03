from dataclasses import dataclass
from .player import ProPlayer

@dataclass
class Team:
    name: str
    league: str
    solo: ProPlayer
    jungle: ProPlayer
    mid: ProPlayer
    support: ProPlayer
    ADC: ProPlayer