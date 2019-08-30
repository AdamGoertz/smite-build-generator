from .context import Player, ProPlayer
import pytest
from dataclasses import FrozenInstanceError

def test_player_creation():
    p = Player("Name", 1)

    assert isinstance(p, Player)
    assert p.name == "Name"
    assert p.id == 1

def test_pro_player_creation():
    pp = ProPlayer("ProName", 2, "Team", "Role")

    assert isinstance(pp, ProPlayer)
    assert pp.name == "ProName"
    assert pp.id == 2
    assert pp.team == "Team"
    assert pp.role == "Role"

def test_player_editable():
    p = Player("Name", 1)

    with pytest.raises(FrozenInstanceError):
        p.name = "NewName"

def test_pro_player_editable():
    pp = ProPlayer("Name", 1, "Team", "Role")

    with pytest.raises(FrozenInstanceError):
        pp.team = "NewTeam"

