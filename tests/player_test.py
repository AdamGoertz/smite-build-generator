from .context import Player
import pytest
from dataclasses import FrozenInstanceError

def test_player_creation():
    p = Player("Name", 1)

    assert isinstance(p, Player)
    assert p.name == "Name"
    assert p.id == 1


def test_player_editable():
    p = Player("Name", 1)

    with pytest.raises(FrozenInstanceError):
        p.name = "NewName"
