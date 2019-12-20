from abc import ABC, abstractmethod
from data_objects.item import Item
from typing import Collection

class Map(ABC):
    @abstractmethod
    def map(self, items: Collection[Item]) -> Collection[Item]:
        return items


class IdentityMap(Map):
    """Combines multiple items which should be treated as a single item."""

    def __init__(self, items: Collection[Item]):
        item_iter = iter(items)
        # First item is used as replacement
        self.replacement = next(item_iter)
        # All remaining items are targets to be replaced
        self.targets = tuple(item_iter)

    def map(self, items: Collection[Item]) -> Collection[Item]:
        return [(item if item not in self.targets else self.replacement)for item in items]

