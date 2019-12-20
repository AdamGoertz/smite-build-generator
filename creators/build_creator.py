from typing import Collection, List
from trackers.build_tracker import BuildTracker
from filters.filter import Filter
from data_objects.item import Item

class BuildCreator:
    def __init__(self, build_tracker: BuildTracker, filters: Collection[Filter] = tuple()):
        self.build_tracker = build_tracker
        self.filters = filters

    def tracker(self) -> BuildTracker:
        return self.build_tracker

    def get_build(self, item_count: int) -> Collection[Item]:
        if not self.build_tracker.items():
            return None

        build: List[Item] = []

        for _ in range(item_count):
            build.append(self._next_item(build))

        return self._sort_build(build)

    def _filter(self, item: Item, build: Collection[Item]) -> bool:
        return any(map(lambda filter: filter.apply(item, build), self.filters))

    def _sort_build(self, build: Collection[Item]) -> Collection[Item]:
        # Sort according to slot preferences returned by item.get_slots().
        return sorted(build, key=lambda item: self.build_tracker.get(item).get_slots())

    def _next_item(self, build: Collection[Item]) -> Item:
        # Find the item where the sum of the connections between that item and other items in the build is maximized
        # Provided the item is allowed by the filters.
        return max(self.build_tracker.items(),
                   key=lambda item: self.build_tracker.co_occurrences(item, build) if item not in build and not self._filter(item, build) else -1)


class ItemBuildCreator(BuildCreator):
    ITEM_COUNT = 6

    def __init__(self, build_tracker: BuildTracker, filters: Collection[Filter] = tuple()):
        super().__init__(build_tracker, filters)

    def get_build(self) -> Collection[Item]:
        return super().get_build(ItemBuildCreator.ITEM_COUNT)


class RelicBuildCreator(BuildCreator):
    ITEM_COUNT = 2

    def __init__(self, build_tracker: BuildTracker, filters: Collection[Filter] = tuple()):
        super().__init__(build_tracker)

    def get_build(self) -> Collection[Item]:
        return super().get_build(RelicBuildCreator.ITEM_COUNT)