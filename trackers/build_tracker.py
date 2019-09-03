from graphs.weighted_graph import WeightedGraph
from data_objects.item import Item
from trackers.item_tracker import ItemTracker
from typing import Iterable, Any, Dict

class BuildTracker:
    def __init__(self, graph: WeightedGraph, tracker_factory):
        self.graph = graph
        self.tracker_factory = tracker_factory
        self.trackers: Dict[Item, ItemTracker] = {}
        self.matches: int = 0

    def __repr__(self):
        return f'[{", ".join((str(tracker) for tracker in self.trackers.values()))}]'

    def track(self, build: Iterable[Item]):
        self.graph.load_list(build, connection_weight=1)
        
        for i, item in enumerate(build):
            if not self.trackers.get(item, None):
                self.trackers[item] = self.tracker_factory(item)

            self.trackers[item].track(i)

        self.matches += 1
    
    def count(self, item: Item):
        tracker = self.trackers.get(item, None)
        return tracker.count if tracker else 0

    def co_occurrences(self, item: Item, other_items: Iterable[Item]):
        return sum((self.graph.get(item).get(other_item, 0) for other_item in other_items))

    def get(self, item: Item, *, default: Any=None):
        return self.trackers.get(item, default)

    def items(self):
        return self.trackers.keys()

    def get_trackers(self):
        return self.trackers.values()

    def most_common(self):
        return max(self.items(), key=lambda item: self.count(self.get(item)))