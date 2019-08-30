from .context import ItemTracker, Item

def test_track():
    it = ItemTracker(Item("TestItem"))
    it.track(1)

    assert 1 in it.slots
    assert it.count == 1

def test_get_slots():
    it = ItemTracker(Item("TestItem"))
    it.track(1)
    it.track(1)
    it.track(2)

    assert it.get_slots() == [1, 2]

def test_get_slots_empty():
    it = ItemTracker(Item("TestItem"))
    assert it.get_slots() == []