from .context import BuildTracker, Item
from unittest.mock import patch, Mock

@patch('filters.item_map.ItemMap')
@patch('trackers.item_tracker.ItemTracker')
@patch('graphs.weighted_graph.WeightedGraph')
def test_track(WeightedGraph, ItemTracker, ItemMap):
    item1 = Item("Item_1")
    items = [item1]
    tracker_factory = Mock(return_value=ItemTracker)
    ItemMap.map.return_value = items
    ItemTracker.count = 1
    maps = [ItemMap]

    bt = BuildTracker(WeightedGraph, tracker_factory, maps)
    bt.track(items)


    WeightedGraph.load_list.assert_called()
    ItemMap.map.assert_called()
    ItemTracker.track.assert_called()
    assert bt.get(item1) == ItemTracker
    assert bt.matches == 1
    assert bt.count(item1)




