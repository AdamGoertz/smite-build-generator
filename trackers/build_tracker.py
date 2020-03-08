from graphs.weighted_graph import WeightedGraph
from data_objects.item import Item
from trackers.item_tracker import ItemTracker
from typing import Collection, Dict, Type, Sequence
from filters.item_map import ItemMap

class BuildTracker:
    def __init__(self, graph: WeightedGraph, tracker_factory: Type[ItemTracker], item_maps: Collection[ItemMap]):
        self.graph = graph
        self.tracker_factory = tracker_factory
        self.trackers: Dict[Item, ItemTracker] = {}
        self.item_maps = item_maps
        self.matches: int = 0

    def __repr__(self):
        return f'[{", ".join((str(tracker) for tracker in self.trackers.values()))}]'

    def track(self, build: Sequence[Item]):
        # Apply item mappings
        for map in self.item_maps:
            build = map.map(build)

        self.graph.load_list(build, connection_weight=1)

        for i, item in enumerate(build):
            if not self.trackers.get(item, None):
                self.trackers[item] = self.tracker_factory(item)

            self.trackers[item].track(i)

        self.matches += 1
    
    def count(self, item: Item) -> int:
        tracker = self.trackers.get(item, None)
        return tracker.count if tracker else 0

    def co_occurrences(self, item: Item, other_items: Collection[Item]) -> int:
        return sum((self.graph.get(item).get(other_item, 0) for other_item in other_items))

    def get(self, item: Item) -> ItemTracker:
        return self.trackers.get(item, self.tracker_factory(item))

