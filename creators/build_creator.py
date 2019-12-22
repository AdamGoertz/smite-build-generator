from typing import Collection, List, Sequence
from trackers.build_tracker import BuildTracker
from filters.filter import Filter
from data_objects.item import Item

class BuildCreator:
    def __init__(self, item_count: int, filters: Collection[Filter] = tuple()):
        self.filters = filters
        self.item_count = item_count

    def get_build(self, build_tracker: BuildTracker) -> Sequence[Item]:
        build: List[Item] = []

        for _ in range(self.item_count):
            build.append(self._next_item(build_tracker, build))

        return BuildCreator._sort_build(build_tracker, build)

    def _filter(self, item: Item, build: Collection[Item]) -> bool:
        """Returns True if 'item' is filtered by any of the stored filters, otherwise False."""
        return any(map(lambda filter: filter.apply(item, build), self.filters))

    def _next_item(self, build_tracker: BuildTracker, build: Collection[Item]) -> Item:
        """Find the item where the sum of the connections between that item and other items in the build is maximized, provided the item is allowed by the filters."""
        return max(build_tracker.items(),
                   key=lambda item: build_tracker.co_occurrences(item, build) if not self._filter(item, build) else -1)

    @staticmethod
    def _sort_build(build_tracker: BuildTracker, build: Collection[Item]) -> Sequence[Item]:
        """Sort according to slot preferences returned by item.get_slots()."""
        return sorted(build, key=lambda item: build_tracker.get(item).get_slots())

class ItemBuildCreator(BuildCreator):
    ITEM_COUNT: int = 6

    def __init__(self, filters: Collection[Filter] = tuple()):
        super().__init__(ItemBuildCreator.ITEM_COUNT, filters)


class RelicBuildCreator(BuildCreator):
    ITEM_COUNT: int = 2

    def __init__(self, filters: Collection[Filter] = tuple()):
        super().__init__(RelicBuildCreator.ITEM_COUNT, filters)
