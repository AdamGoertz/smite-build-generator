from dataclasses import dataclass
from data_objects.item import Item
from typing import Tuple

@dataclass
class Build:
    items: Tuple[Item]
    relics: Tuple[Item]

    def __str__(self):
        return (f'Items: {", ".join(map(str, self.items))}\n'
                f'Relics: {", ".join(map(str, self.relics))}')