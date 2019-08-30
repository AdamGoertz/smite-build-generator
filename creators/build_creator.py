from typing import Iterable
from trackers.build_tracker import BuildTracker
from data.item import Item

class BuildCreator:
    def __init__(self, build_tracker: BuildTracker):
        self.build_tracker = build_tracker

    def tracker(self):
        return self.build_tracker

    def get_build(self, item_count: int):
        if not self.build_tracker.items():
            return None

        # Initialize build with most common item
        build = [self.build_tracker.most_common()]

        for j in range(item_count-1):
            build.append(self._next_item(build))

        return self._sort_build(build)

    def _sort_build(self, build: Iterable[Item]):
        # Sort according to slot preferences returned by item.get_slots().
        return sorted(build, key=lambda item: self.build_tracker.get(item).get_slots())

    def _next_item(self, build: Iterable[Item]):
        # Find the item where the sum of the connections between that item and items in the build is maximized TODO: Resolve ties using total frequency
        return max(self.build_tracker.items(), key=lambda item: self.build_tracker.co_occurrences(item, build) if item not in build else -1)


class ItemBuildCreator(BuildCreator):
    ITEM_COUNT = 6

    def __init__(self, build_tracker: BuildTracker):
        super().__init__(build_tracker)

    def get_build(self):
        return super().get_build(ItemBuildCreator.ITEM_COUNT)


class RelicBuildCreator(BuildCreator):
    ITEM_COUNT = 2

    def __init__(self, build_tracker: BuildTracker):
        super().__init__(build_tracker)

    def get_build(self):
        return super().get_build(RelicBuildCreator.ITEM_COUNT)