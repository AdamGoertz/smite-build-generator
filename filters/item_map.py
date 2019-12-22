from abc import ABC, abstractmethod
from data_objects.item import Item
from typing import Sequence, Collection

class ItemMap(ABC):
    """An abstract class for applying a mapping to a collection of items. Mappings may replace, remove, combine items, etc.
    Map implementations may produce a copy or be done in-place."""

    @abstractmethod
    def map(self, items: Sequence[Item]) -> Sequence[Item]:
        return items


class IdentityMap(ItemMap):
    """Maps a collection of items to a single identity. When any of the specified items is encountered, it will be mapped to a single name.

    This prevents items with multiple names (e.g. Book of Thoth vs Evolved Book of Thoth) from being under-counted."""

    def __init__(self, items: Collection[Item]):
        item_iter = iter(items)
        # First item is used as replacement
        self.replacement = next(item_iter)
        # All remaining items are targets to be replaced
        self.targets = tuple(item_iter)

    def map(self, items: Sequence[Item]) -> Sequence[Item]:
        """Replace all target items with a single equivalent item."""
        return [(item if item not in self.targets else self.replacement) for item in items]






