from .context import ExclusionFilter, MutualExclusionFilter, Item

def test_exclusion_filter_true():
    filter = ExclusionFilter((Item("Test1"), Item("Test2")))
    assert filter.apply(Item("Test1"))
    assert filter.apply(Item("Test2"))

def test_exclusion_filter_false():
    filter = ExclusionFilter((Item("Test1"), Item("Test2")))
    assert not filter.apply(Item("Test3"))



def test_mutual_exclusion_filter_true():
    filter = MutualExclusionFilter((Item("Test1"), Item("Test2")))
    current_items = (Item("Test1"), Item("Test3"))
    assert filter.apply(Item("Test2"), current_items)

def test_mutual_exclusion_filter_false():
    filter = MutualExclusionFilter((Item("Test1"), Item("Test2")))

    # Case where new item is not in mutex group
    current_items1 = (Item("Test1"), Item("Test3"))
    assert not filter.apply(Item("Test4"), current_items1)

    # Case where current items does not yet contain a member of the mutex group
    current_items2 = (Item("Test3"), Item("Test4"))
    assert not filter.apply(Item("Test1"), current_items2)


