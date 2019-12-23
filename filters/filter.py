from typing import Collection
from abc import ABC, abstractmethod
from data_objects.item import Item

class Filter(ABC):
    @abstractmethod
    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        """Return True if item meets filter condition (should be filtered), False otherwise."""
        return False


# Filter class concrete implementations
class ExclusionFilter(Filter):
    def __init__(self, excluded_items: Collection[Item] = set()):
        self.excluded_items = set(excluded_items)

    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        return item in self.excluded_items


class MutualExclusionFilter(Filter):
    def __init__(self, mutually_exclusive_items: Collection[Item] = set()):
        self.mutex_items = set(mutually_exclusive_items)

    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        # Return True if the new item is in the mutex group, and the build already contains one+ item(s) in the mutex group.
        return item in self.mutex_items and not self.mutex_items.isdisjoint(set(other_items))


class DuplicateExclusionFilter(Filter):
    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        return item in other_items


class PriorityFilter(Filter):
    def __init__(self, prioritized_items: Collection[Item] = set()):
        self.prioritized_items = set(prioritized_items)

    def apply(self, item: Item, other_items: Collection[Item] = set()) -> bool:
        """Return True (filter the item) if
            * not all the prioritized items have been added yet, and
            * the new item is not prioritized, and
            * all the items added so far have been prioritized items.

            The third condition ensures that the system does not continue to search for prioritized items if no more appear in the build data.
            (i.e. if at any point the system fails to find any of the prioritized items, a non-priority item will be added,
            causing the third condition to evaluate to False, allowing the system to process non-priority items as normal)
        """

        return len(other_items) < len(self.prioritized_items) \
               and item not in self.prioritized_items \
               and all(check_item in self.prioritized_items for check_item in other_items)

