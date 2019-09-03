from .context import BuildTracker, Item
from unittest.mock import patch, Mock

@patch('trackers.item_tracker.ItemTracker')
@patch('graphs.weighted_graph.WeightedGraph')
def test_track(WeightedGraph, ItemTracker):
    item1 = Item("Item_1")
    item2 = Item("Item_2")
    tracker_factory = Mock(return_value=ItemTracker)
    bt = BuildTracker(WeightedGraph, tracker_factory)

    bt.track((item1, item2))

    WeightedGraph.load_list.assert_called()
    ItemTracker.track.assert_called()
    assert bt.matches == 1

@patch('trackers.item_tracker.ItemTracker')
@patch('graphs.weighted_graph.WeightedGraph')
def test_count(WeightedGraph, ItemTracker):
    item1 = Item("Item_1")
    item2 = Item("Item_2")
    ItemTracker.count = 1
    tracker_factory = Mock(return_value=ItemTracker)
    bt = BuildTracker(WeightedGraph, tracker_factory)

    bt.track([item1])
    assert bt.count(item1) == 1
    assert bt.count(item2) == 0


