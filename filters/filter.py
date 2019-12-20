from typing import Collection, Any
from abc import ABC, abstractmethod
from data_objects.item import Item

class Filter(ABC):
    @abstractmethod
    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        """Return True if item meets filter condition (should be filtered), False otherwise."""
        pass


# Filter class concrete implementations
class ExclusionFilter(Filter):
    def __init__(self, excluded_items: Collection[Item] = set()):
        self.excluded_items = set(excluded_items)

    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        return item in self.excluded_items


class MutualExclusionFilter(Filter):
    def __init__(self, mutually_exclusive_items: Collection[Item] = set()):
        self.mutex_items = set(mutually_exclusive_items)

    def apply(self, item: Item, other_items: Collection[Item]) -> bool:
        # Return True if the new item is in the mutex group, and the build already contains one+ item(s) in the mutex group.
        return True if (self.mutex_items & set(other_items)) and item in self.mutex_items else False

