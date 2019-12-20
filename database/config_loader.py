import json
from data_objects.item import Item
from abc import ABC, abstractmethod
from typing import Type, Tuple, Any

class ConfigDataLoader(ABC):
    @abstractmethod
    def load(self, filename: str):
        pass

class ItemLoader(ConfigDataLoader):
    def __init__(self, item_factory: Type[Item]):
        self.item_factory = item_factory

    def load(self, filename: str) -> Tuple[Item]:
        with open(filename, 'r') as f:
            return tuple(map(self.item_factory, json.load(f)))


