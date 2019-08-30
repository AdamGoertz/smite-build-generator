from .context import Item
import pytest
from dataclasses import FrozenInstanceError

def test_item_creation():
    i = Item("Test")
    assert isinstance(i, Item) and i.name == "Test"

def test_item_rename():
    i = Item("Test")
    with pytest.raises(FrozenInstanceError):
        i.name = "NewName"
