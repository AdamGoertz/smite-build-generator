from .context import IdentityMap, Item


def test_identity_map_equivalent_items():
    map = IdentityMap([Item("test1"), Item("test2")])
    items = [Item("test2"), Item("test3")]
    items = map.map(items)
    assert items == [Item("test1"), Item("test3")]


def test_identity_map_unequivalent_items():
    map = IdentityMap([Item("test1"), Item("test2)")])
    items = [Item("test3")]
    items = map.map(items)
    assert items == [Item("test3")]