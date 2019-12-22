from dataclasses import dataclass
from data_objects.item import Item
from typing import Sequence

@dataclass
class Build:
    items: Sequence[Item]
    relics: Sequence[Item]

    def __str__(self):
        return (f'Items: {", ".join(map(str, self.items))}\n'
                f'Relics: {", ".join(map(str, self.relics))}')